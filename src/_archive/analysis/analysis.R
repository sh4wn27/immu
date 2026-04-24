# analysis.R
# Publication-ready statistical analysis for the stealth-polymer HSCT study.
# Columns match docs/phase0/data_capture_templates.md (T-00 through T-13).
#
# Required packages: tidyverse, readxl, survival, survminer, flowCore, pwr, emmeans, lme4
# Install once: install.packages(c("tidyverse","readxl","survival","survminer","pwr","emmeans","lme4"))
#               BiocManager::install("flowCore")

suppressPackageStartupMessages({
  library(tidyverse)
  library(readxl)
  library(survival)
  library(survminer)
  library(emmeans)
  library(lme4)
  library(pwr)
})

set.seed(20260815)

# ---- Paths --------------------------------------------------------------
DATA_ROOT <- Sys.getenv("DATA_ROOT", "data/sheets")
OUT_FIG   <- Sys.getenv("OUT_FIG",   "data/derived/figures")
OUT_TAB   <- Sys.getenv("OUT_TAB",   "data/derived/tables")
dir.create(OUT_FIG, recursive = TRUE, showWarnings = FALSE)
dir.create(OUT_TAB, recursive = TRUE, showWarnings = FALSE)

# ---- Schema validation --------------------------------------------------
required_cols <- list(
  T04_mlr = c("plate_id","well","stimulator_type","et_ratio","biological_rep",
              "technical_rep","cfse_divided_pct","proliferation_index",
              "ifn_gamma_pgmL","il_2_pgmL"),
  T05_cfu = c("dish_id","cell_source","input_cells","biological_rep","technical_rep",
              "cfu_gemm","cfu_gm","bfu_e","cfu_total"),
  T08_animals = c("mouse_id","group","sex","weight_d0_g","endpoint_date","endpoint_reason"),
  T09_gvhd = c("mouse_id","date","day_post_tx","total_gvhd"),
  T10_chim = c("mouse_id","day_post_tx","cd45_1_donor_pct","cd45_2_host_pct"),
  T11_ivis = c("mouse_id","day_post_tx","radiant_efficiency_liver",
               "radiant_efficiency_spleen","radiant_efficiency_hindlimb_BM",
               "pct_initial_signal"),
  T12_serum = c("mouse_id","alt_u_L","ast_u_L","bun_mgdL","creatinine_mgdL"),
  T13_histo = c("mouse_id","organ","inflammation_score","composite_organ_score")
)

validate_schema <- function(df, table_key) {
  missing <- setdiff(required_cols[[table_key]], names(df))
  if (length(missing)) {
    stop(sprintf("Missing required columns in %s: %s",
                 table_key, paste(missing, collapse = ", ")))
  }
  df
}

load_sheet <- function(filename, table_key, sheet = 1) {
  path <- file.path(DATA_ROOT, filename)
  if (!file.exists(path)) {
    warning(sprintf("Data file not found: %s — returning empty tibble", path))
    return(tibble::tibble())
  }
  df <- readxl::read_excel(path, sheet = sheet)
  validate_schema(df, table_key)
}

# ---- MLR analysis (Aim 2) -----------------------------------------------
analyze_mlr <- function(mlr_df) {
  mlr_df <- mlr_df %>%
    mutate(stimulator_type = factor(stimulator_type,
      levels = c("syngeneic","uncoated-alloB","PEG-alloB","PCB-alloB",
                 "polyclonal","none")))
  grouped <- mlr_df %>%
    group_by(stimulator_type, et_ratio, biological_rep) %>%
    summarise(
      prolif = mean(proliferation_index, na.rm = TRUE),
      ifng   = mean(ifn_gamma_pgmL, na.rm = TRUE),
      il2    = mean(il_2_pgmL, na.rm = TRUE),
      .groups = "drop"
    )
  # One-way ANOVA + Tukey within each E:T ratio, proliferation index as primary
  res <- grouped %>%
    group_by(et_ratio) %>%
    group_modify(~ {
      fit <- aov(prolif ~ stimulator_type, data = .x)
      emm <- emmeans::emmeans(fit, "stimulator_type")
      pairs <- as.data.frame(pairs(emm, adjust = "tukey"))
      pairs
    }) %>% ungroup()
  list(anova_pairs = res, summary = grouped)
}

mlr_suppression_pct <- function(grouped) {
  base <- grouped %>% filter(stimulator_type == "uncoated-alloB") %>%
    group_by(et_ratio) %>% summarise(uncoated = mean(prolif))
  grouped %>% left_join(base, by = "et_ratio") %>%
    mutate(suppression_pct = 100 * (uncoated - prolif) / uncoated) %>%
    filter(stimulator_type %in% c("PEG-alloB","PCB-alloB"))
}

# ---- CFU analysis (Aim 2) -----------------------------------------------
analyze_cfu <- function(cfu_df) {
  cfu_df <- cfu_df %>%
    mutate(cell_source = factor(cell_source,
      levels = c("uncoated","PEG","PCB","human-CD34")))
  summ <- cfu_df %>%
    group_by(cell_source, biological_rep) %>%
    summarise(total = mean(cfu_total), .groups = "drop")
  # Mixed model: biological_rep as random effect to handle blocking
  fit <- lme4::lmer(cfu_total ~ cell_source + (1 | biological_rep), data = cfu_df)
  list(summary = summ, model = fit)
}

cfu_retention_pct <- function(summ) {
  base <- summ %>% filter(cell_source == "uncoated") %>%
    summarise(uncoated = mean(total)) %>% pull(uncoated)
  summ %>% mutate(retention_pct = 100 * total / base)
}

# ---- Chimerism (Aim 3 primary) -----------------------------------------
analyze_chimerism <- function(chim_df, animals_df) {
  chim_df <- chim_df %>% left_join(animals_df %>% select(mouse_id, group),
                                   by = "mouse_id") %>%
    mutate(group = factor(group,
      levels = c("A-syn","B-uncoated","C-PEG","D-PCB","E-imaging")))
  # Primary endpoint: chimerism at day 28 (week 4), t-test B vs C, B vs D
  wk4 <- chim_df %>% filter(day_post_tx %in% c(27, 28, 29)) %>%
    group_by(mouse_id, group) %>%
    summarise(donor = mean(cd45_1_donor_pct), .groups = "drop")
  t_PEG <- t.test(donor ~ group, data = wk4 %>% filter(group %in% c("B-uncoated","C-PEG")))
  t_PCB <- t.test(donor ~ group, data = wk4 %>% filter(group %in% c("B-uncoated","D-PCB")))
  # Repeated-measures across timepoints
  rm_fit <- lme4::lmer(cd45_1_donor_pct ~ group * day_post_tx + (1 | mouse_id),
                       data = chim_df)
  list(wk4 = wk4, t_PEG = t_PEG, t_PCB = t_PCB, rm_model = rm_fit)
}

# ---- GvHD score --------------------------------------------------------
analyze_gvhd <- function(gvhd_df, animals_df) {
  gvhd_df <- gvhd_df %>% left_join(animals_df %>% select(mouse_id, group),
                                   by = "mouse_id")
  # Non-parametric Mann-Whitney per day between coated vs uncoated allo
  test_day <- function(d) {
    sub <- gvhd_df %>% filter(day_post_tx == d,
                              group %in% c("B-uncoated","C-PEG","D-PCB"))
    bind_rows(
      tibble::tibble(day = d, comparison = "B-vs-C",
             p = suppressWarnings(wilcox.test(total_gvhd ~ group,
               data = sub %>% filter(group %in% c("B-uncoated","C-PEG")))$p.value)),
      tibble::tibble(day = d, comparison = "B-vs-D",
             p = suppressWarnings(wilcox.test(total_gvhd ~ group,
               data = sub %>% filter(group %in% c("B-uncoated","D-PCB")))$p.value))
    )
  }
  days <- c(7, 14, 21, 28, 35, 42)
  do.call(bind_rows, lapply(days, test_day))
}

# ---- Survival ----------------------------------------------------------
analyze_survival <- function(animals_df) {
  df <- animals_df %>%
    mutate(
      time = as.numeric(endpoint_date - irradiation_date),
      event = as.integer(endpoint_reason != "scheduled-d42")
    )
  fit <- survfit(Surv(time, event) ~ group, data = df)
  lr <- survdiff(Surv(time, event) ~ group, data = df)
  list(km = fit, logrank = lr)
}

# ---- IVIS clearance ----------------------------------------------------
analyze_ivis <- function(ivis_df) {
  ivis_df %>%
    group_by(day_post_tx) %>%
    summarise(
      mean_pct = mean(pct_initial_signal, na.rm = TRUE),
      se = sd(pct_initial_signal, na.rm = TRUE) / sqrt(n()),
      .groups = "drop"
    )
}

# ---- Figures -----------------------------------------------------------
theme_paper <- function() {
  theme_bw(base_size = 11) +
    theme(
      panel.grid.minor = element_blank(),
      panel.grid.major = element_line(linewidth = 0.2, color = "grey85"),
      legend.position = "top",
      strip.background = element_blank()
    )
}

fig_chimerism_over_time <- function(chim_df, animals_df, save = TRUE) {
  df <- chim_df %>% left_join(animals_df %>% select(mouse_id, group),
                              by = "mouse_id")
  p <- ggplot(df, aes(day_post_tx, cd45_1_donor_pct, color = group, fill = group)) +
    stat_summary(fun.data = mean_se, geom = "ribbon", alpha = 0.2, color = NA) +
    stat_summary(fun = mean, geom = "line", linewidth = 0.9) +
    stat_summary(fun = mean, geom = "point", size = 2) +
    geom_hline(yintercept = 60, linetype = "dashed", color = "black") +
    labs(x = "Day post-transplant", y = "Donor chimerism (CD45.1⁺ %)",
         color = NULL, fill = NULL) +
    theme_paper()
  if (save) ggsave(file.path(OUT_FIG, "fig5a_chimerism.pdf"), p,
                   width = 5, height = 3.5)
  p
}

fig_gvhd_score <- function(gvhd_df, animals_df, save = TRUE) {
  df <- gvhd_df %>% left_join(animals_df %>% select(mouse_id, group),
                              by = "mouse_id")
  p <- ggplot(df, aes(day_post_tx, total_gvhd, color = group, fill = group)) +
    stat_summary(fun.data = mean_se, geom = "ribbon", alpha = 0.2, color = NA) +
    stat_summary(fun = mean, geom = "line", linewidth = 0.9) +
    labs(x = "Day post-transplant", y = "GvHD composite score (0–10)",
         color = NULL, fill = NULL) +
    theme_paper()
  if (save) ggsave(file.path(OUT_FIG, "fig5b_gvhd.pdf"), p,
                   width = 5, height = 3.5)
  p
}

fig_km_survival <- function(animals_df, save = TRUE) {
  df <- animals_df %>%
    mutate(
      time  = as.numeric(endpoint_date - irradiation_date),
      event = as.integer(endpoint_reason != "scheduled-d42")
    )
  fit <- survfit(Surv(time, event) ~ group, data = df)
  p <- survminer::ggsurvplot(fit, data = df, risk.table = TRUE,
                             conf.int = FALSE, pval = TRUE,
                             xlab = "Day post-transplant", ylab = "Survival")
  if (save) ggsave(file.path(OUT_FIG, "fig5c_survival.pdf"),
                   p$plot + p$table, width = 6, height = 5)
  p
}

fig_ivis_clearance <- function(ivis_df, save = TRUE) {
  summ <- analyze_ivis(ivis_df)
  p <- ggplot(summ, aes(day_post_tx, mean_pct)) +
    geom_ribbon(aes(ymin = mean_pct - se, ymax = mean_pct + se), alpha = 0.2) +
    geom_line(linewidth = 0.9) +
    geom_point(size = 2) +
    geom_hline(yintercept = 5, linetype = "dashed", color = "red") +
    labs(x = "Day post-transplant", y = "% initial polymer signal") +
    theme_paper()
  if (save) ggsave(file.path(OUT_FIG, "fig5d_ivis.pdf"), p,
                   width = 5, height = 3.5)
  p
}

# ---- End-to-end runner -------------------------------------------------
run_all <- function() {
  animals <- load_sheet("T08_animals.xlsx", "T08_animals")
  if (nrow(animals) == 0) {
    message("No data yet — scaffold validated, awaiting bench data.")
    return(invisible(NULL))
  }
  mlr   <- load_sheet("T04_mlr.xlsx",   "T04_mlr")
  cfu   <- load_sheet("T05_cfu.xlsx",   "T05_cfu")
  gvhd  <- load_sheet("T09_gvhd.xlsx",  "T09_gvhd")
  chim  <- load_sheet("T10_chim.xlsx",  "T10_chim")
  ivis  <- load_sheet("T11_ivis.xlsx",  "T11_ivis")
  histo <- load_sheet("T13_histo.xlsx", "T13_histo")

  results <- list(
    mlr      = analyze_mlr(mlr),
    cfu      = analyze_cfu(cfu),
    chim     = analyze_chimerism(chim, animals),
    gvhd     = analyze_gvhd(gvhd, animals),
    survival = analyze_survival(animals),
    ivis     = analyze_ivis(ivis)
  )

  fig_chimerism_over_time(chim, animals)
  fig_gvhd_score(gvhd, animals)
  fig_km_survival(animals)
  fig_ivis_clearance(ivis)

  saveRDS(results, file.path(OUT_TAB, "results.rds"))
  invisible(results)
}

# When invoked from Rscript:
if (sys.nframe() == 0 && identical(commandArgs(trailingOnly = TRUE)[1], "run")) {
  run_all()
}
