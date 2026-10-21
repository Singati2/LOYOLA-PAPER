"""Authoritative list of the files each script of the replay plan must write (paths relative to the repository).

Reviewed by hand from each script's write calls (2026-10-21) and checked against the rewrite counts of the
lab replay of 09ceba8 (verification_logs/lab_09ceba8) and a trace of the short scripts. It is deliberately
NOT derived from the files a run happens to write: colab/pipeline.py compares what a script wrote with this
list and refuses to record the script as OK if a listed file is missing, empty or not rewritten, or if the
script rewrote a tracked file that is listed neither here nor in INCIDENTAL.

An empty list marks a check-only script: its exit status is its whole result and it must write no tracked
file. Every file listed is tracked by git, except the NIST pages, which are never listed (they are read
from the private cache and never kept in the state folder).
"""

EXPECTED = {
    # stage 1
    "external/build_nonane_data.py": ["external/nonane_data.csv", "external/nonane_identity.csv",
                                      "external/nonane_provenance.csv"],
    "external/check_nonane_structures.py": [],
    "external/bp/build_bp_data.py": ["external/bp/bp_data.csv", "external/bp/bp_provenance.csv"],
    "external/bp/build_calorimetric_set.py": ["external/bp/calorimetric_dHvap298_alkanes.csv"],
    "DATA/build_data.py": ["DATA/octane_properties.csv", "DATA/octane_provenance.csv", "DATA/nonane_properties.csv",
                           "DATA/nonane_provenance.csv", "DATA/boiling_points_C6_C10.csv",
                           "DATA/boiling_points_provenance.csv", "DATA/calorimetric_dHvap298_alkanes.csv",
                           "DATA/boiling_points_structures.csv"],
    "audit/check_source_identities.py": [],
    # stage 2
    "structural/minimality_check.py": ["structural/minimality_check_out.txt"],
    "structural/extremal_trees_check.py": ["structural/extremal_trees_check_out.txt"],
    "structural/sumconn_pair_check.py": ["structural/sumconn_pair_check_out.txt"],
    "structural/count_dimension_check.py": ["structural/count_dimension_check_out.txt"],
    "structural/fractional_points.py": ["structural/fractional_points_out.txt"],
    "structural/chi_floor.py": ["structural/chi_floor_out.txt"],
    "multi_order_degeneracy.py": ["multi_order_degeneracy.csv"],
    "redundancy_collisions.py": ["bid_collision_table.csv", "descriptor_correlations.csv", "pca_spectrum.csv"],
    "audit/check_mathematics.py": [],
    "structural/structural_checks.py": ["structural/structural_checks_out.txt"],
    "structural/hp_counts.py": ["structural/hp_counts_out.txt"],
    "structural/exact_ties.py": ["structural/exact_ties_out.txt"],
    # stage 3
    "ablation_gm_vs_lo.py": ["ablation_perfold.csv", "ablation_summary.csv"],
    "source_sensitivity.py": ["omega_source_sensitivity_v35.csv", "entropy_source_sensitivity_v36.csv",
                              "entropy_api44_sensitivity_v41.csv"],
    "fgd_structure_sensitivity.py": ["fgd_published_control.csv", "fgd_structure_sensitivity_decanes.csv"],
    "tmb_dhvap_audit.py": ["tmb_dhvap_audit.csv"],
    "tuning_pool_seed_sweep.py": ["tuning_pool_seed_sweep_out.txt"],
    "generate_loyola_v35_figures.py": ["lo_sensitivity_prediction_correlations.csv",
                                       "lo_sensitivity_degeneracy_order10_trees.csv",
                                       "lo_sensitivity_structure_sensitivity_decanes.csv",
                                       "figures/fig_lo_prediction_correlation_heatmap_v3.pdf",
                                       "figures/fig_lo_degeneracy_order10_trees_v2.pdf"],
    "tmb_exclusion_sensitivity.py": ["dhvap_tmb_exclusion_v36.csv", "dhvap_tmb_exclusion_summary_v36.csv"],
    "expanded_robustness_v35.py": ["expanded_robustness_v35.csv", "expanded_robustness_summary_v35.csv"],
    "constancy_test_check.py": ["constancy_test_check_out.txt"],
    "ablation_robustness.py": ["ablation_robustness.csv"],
    "verify_loyola_v35.py": ["verify_loyola_v35_results.csv", "verify_loyola_v35_folds.csv"],
    # stage 4
    "external/baselines.py": ["external/baselines_octane.csv"],
    "external/baselines.py --dataset nonane": ["external/baselines_nonane.csv"],
    "external/nonane_validation.py": ["external/nonane_validation_seeds.csv", "external/nonane_validation_summary.csv"],
    "external/transfer_exploratory.py": ["external/transfer_exploratory.csv", "external/transfer_exploratory_summary.csv"],
    "external/uncertainty_exploratory.py": ["external/uncertainty_exploratory.csv"],
    "external/wide_box_diagnostics.py": ["external/wide_box_diagnostics_out.txt"],
    "external/box_sensitivity.py": ["external/box_sensitivity.csv", "external/box_sensitivity_summary.csv"],
    "external/nonane_tb_conflict.py": ["external/nonane_tb_conflict_out.txt"],
    "external/make_box_table.py": ["external/box_table_rows.tex"],
    "external/make_v37_table.py": ["external/v37_classical_fixed.csv", "external/v37_table_rows.tex"],
    # stage 5
    "external/bp/coverage_bias.py": ["external/bp/coverage_bias.csv"],
    "external/bp/wiener_baseline.py": ["external/bp/wiener_baseline_out.txt"],
    "external/bp/bp_tests.py": ["external/bp/bp_results_seeds.csv", "external/bp/bp_results_summary.csv",
                                "external/bp/bp_baselines.csv"],
    "external/bp/make_bp_table.py": ["external/bp/bp_table_rows.tex"],
    "external/bp/selection_resampling.py": ["external/bp/selection_resampling.csv",
                                            "external/bp/selection_resampling_summary.csv"],
    # stage 6
    "audit/final/scripts/claim_provenance.py": ["audit/final/scripts/claim_provenance_ledger.csv",
                                                "audit/final/scripts/claim_provenance_out.txt"],
    "audit/v4030/math_independent.py": ["audit/v4030/math_independent_out.txt"],
    "audit/v4030/table2_independent.py": ["audit/v4030/table2_independent_out.txt"],
    "audit/v4030/leakage_probe.py": ["audit/v4030/leakage_probe_out.txt"],
    "audit/v4030/feature_leakage_probe.py": ["audit/v4030/feature_leakage_probe_out.txt"],
    "audit/v4030/uncertain_source_sensitivity.py": ["audit/v4030/sensitivity_filters.csv", "audit/v4030/sensitivity_octane.csv",
                                                    "audit/v4030/sensitivity_bp.csv",
                                                    "audit/v4030/uncertain_source_sensitivity_out.txt"],
    "audit/final/scripts/counterattack_v4030.py": ["audit/final/scripts/counterattack_v4030_out.txt"],
    "audit/final/scripts/bp_duplicate_sensitivity.py": ["audit/final/scripts/bp_duplicate_sensitivity_out.txt"],
    "audit/v4030/gamma_strict.py": ["audit/v4030/gamma_strict_out.txt", "audit/v4030/gamma_strict_seeds.csv"],
    # stage 7
    "audit/final/scripts/press_size_probe.py": ["audit/final/scripts/press_size_probe_out.txt"],
    "audit/v4030/refit_stability.py": ["audit/v4030/refit_stability_out.txt", "audit/v4030/refit_subsample_raw.csv"],
    "audit/v4030/sensitivity_followup.py": ["audit/v4030/sensitivity_followup_out.txt", "audit/v4030/sensitivity_composition.csv",
                                            "audit/v4030/sensitivity_decomposition.csv"],
    # stage 8
    "audit/check_exploratory_outputs.py": [],
    "external/test_regressions.py": [],
    "external/test_baselines.py": [],
    "prose_numbers_check.py": [],
}

# Tracked files a script may rewrite besides its listed outputs, each with the reason. A rewritten file in this
# list must still end identical to the commit; otherwise the run is not OK.
INCIDENTAL = {}
