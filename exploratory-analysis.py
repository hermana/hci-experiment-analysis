# ========================================
# Python scripts for 866 example analyses
# ========================================

# ========================================
# 0.0 Setup
# ========================================

# Install (once) if needed:
# pip install pandas numpy matplotlib pingouin scipy statsmodels rpy2

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Stats helpers
import scipy.stats as st
import pingouin as pg  # repeated-measures ANOVA, pairwise tests

# (Optional) for ART via R's ARTool from Python
# Make sure R + ARTool are installed; then set R_HOME if needed.
# In R: install.packages("ARTool")
try:
    import rpy2.robjects as ro
    from rpy2.robjects import pandas2ri
    pandas2ri.activate()
    R_AVAILABLE = True
except Exception:
    R_AVAILABLE = False

# A nicer visual theme for charts (roughly similar to ggplot's "theme_bw")
plt.rcParams.update({
    "figure.dpi": 120,
    "font.size": 12,
    "axes.edgecolor": "#e0e0e0",
    "axes.linewidth": 0.7,
    "grid.color": "#e0e0e0",
    "grid.linewidth": 0.5,
    "axes.grid": True,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.autolayout": True,
})

# ========================================
# Utilities roughly analogous to ezPrecis / ezDesign
# ========================================

def precis(df: pd.DataFrame, name="data"):
    print(f"\n=== precis({name}) ===")
    print(df.info())
    print("\nHead:\n", df.head())
    print("\nDescribe (numeric):\n", df.describe(numeric_only=True))
    print("\nDtypes:\n", df.dtypes)

def ez_design(df: pd.DataFrame, x: str, y: str):
    print(f"\n=== ezDesign x={x}, y={y} ===")
    ct = pd.crosstab(df[y], df[x])
    print(ct)
    return ct

# Standard error helper
def se(series: pd.Series):
    s = series.dropna()
    return s.std(ddof=1) / np.sqrt(len(s)) if len(s) > 0 else np.nan


# ========================================
# Example 1: interface A vs B, DV=completion time
# One IV, so a "one-way" within-subjects test
# ========================================

# ---------------------------------------
# 1.1 Read the data from disk
# ---------------------------------------

ctData = pd.read_csv("example-1.tsv", sep="\t")  # read_tsv
print(ctData.head())
print(ctData.columns.tolist())

# ---------------------------------------
# 1.2 Check the data and reformat if needed
# ---------------------------------------

# rename columns (method -> interface)
ctData = ctData.rename(columns={"method": "interface"})
print(ctData.columns.tolist())

# Factor-like conversion: keep original numeric id, add PID as categorical
ctData["PID"] = ctData["id"].astype("category")
ctData["interface"] = ctData["interface"].astype("category")

precis(ctData, "ctData")

# Check whether we have all of our data (design balance)
ez_design(ctData, x="interface", y="id")

# Filtering rows (e.g., remove incompletes)
print("Unique PIDs before filter:", ctData["PID"].nunique())
incompletes = [11, 12]
ctData = ctData[~ctData["PID"].isin(incompletes)].copy()
print("Unique PIDs after filter:", ctData["PID"].nunique())
ez_design(ctData, x="interface", y="PID")
precis(ctData, "ctData (filtered)")

# ---------------------------------------
# Outliers (cap at mean + 3*SD or a fixed cap)
# ---------------------------------------

# Quick look for weird values (scatter by participant)
plt.figure()
for pid, sub in ctData.groupby("PID"):
    plt.scatter([pid] * len(sub), sub["ct"], s=16)
plt.xlabel("PID")
plt.ylabel("ct")
plt.title("CT by Participant (jittered categories)")
plt.xticks(rotation=90)
plt.savefig("ct-by-pid.png")
plt.close()

# Compute 3 SD cap
ctCap_auto = ctData["ct"].mean() + 3 * ctData["ct"].std(ddof=1)
print("Auto 3*SD cap:", round(ctCap_auto, 3))

# Apply fixed cap like in R (ctCap <- 20.0)
ctCap = 20.0
num_capped = (ctData["ct"] > ctCap).sum()
ctData.loc[ctData["ct"] > ctCap, "ct"] = ctCap
print(f"CT cap is {ctCap}. {num_capped} rows were capped for CT.")

# (Optional) remove outliers by z-score > 3 (analog to remove_sd_outlier)
# Keep only within 3 SD
z = (ctData["ct"] - ctData["ct"].mean()) / ctData["ct"].std(ddof=1)
ctData_no_outliers = ctData.loc[z.abs() <= 3].copy()
# Re-check design if you use ctData_no_outliers instead
ez_design(ctData_no_outliers, x="interface", y="PID")

# ---------------------------------------
# 1.3 Summary stats by interface
# ---------------------------------------

ctSummary = (
    ctData.groupby("interface", observed=True)["ct"]
    .agg(mean="mean", sd=lambda s: s.std(ddof=1), count="size")
    .reset_index()
)
ctSummary["se"] = ctSummary["sd"] / np.sqrt(ctSummary["count"])
print("\nctSummary:\n", ctSummary)

# ---------------------------------------
# 1.4 ANOVA: effect of interface on ct (within-subjects)
# ---------------------------------------
# pingouin requires long format with columns: subject, within, dv
ct_anova = pg.rm_anova(data=ctData, dv="ct", within="interface", subject="id", detailed=True, effsize="np2")
print("\nRepeated-measures ANOVA (interface -> ct):\n", ct_anova)

# ========================================
# 1.5 Simple plot of the data
# ========================================

# Mean ± SE by interface
plt.figure()
plt.bar(ctSummary["interface"].astype(str), ctSummary["mean"])
plt.errorbar(
    x=np.arange(len(ctSummary)),
    y=ctSummary["mean"],
    yerr=ctSummary["se"],
    fmt="none",
    capsize=6,
)
plt.xlabel("Interface")
plt.ylabel("Completion Time (sec)")
plt.title("CT by Interface (mean ± SE)")
plt.savefig("ct-by-interface.png")
plt.close()

# ========================================
# 1.6 Better plot (labels/width similar to ggplot variant)
# ========================================

plt.figure()
bars = plt.bar(ctSummary["interface"].astype(str), ctSummary["mean"], width=0.6)
plt.errorbar(
    x=np.arange(len(ctSummary)),
    y=ctSummary["mean"],
    yerr=ctSummary["se"],
    fmt="none",
    capsize=6,
)
plt.xlabel("Interface")
plt.ylabel("Completion Time (sec)")
plt.title("CT by Interface (mean ± SE)")
plt.savefig("ct-by-interface-2.png")
plt.close()


# ========================================
# Example 2: four conditions (A,B,C,D); DV = completion time
# ========================================

# ---------------------------------------
# 2.1 Read the data from disk
# ---------------------------------------

ctData2 = pd.read_csv("four-conditions.log", sep="\t")
print(ctData2.head())

# ---------------------------------------
# 2.2 Check the data and reformat if needed
# ---------------------------------------

ctData2 = ctData2.rename(columns={"method": "interface"})
ctData2["id"] = ctData2["id"].astype("category")
ctData2["interface"] = ctData2["interface"].astype("category")

precis(ctData2, "ctData2")
ez_design(ctData2, x="interface", y="id")

# ---------------------------------------
# 2.3 Summary stats by interface
# ---------------------------------------

ctSummary2 = (
    ctData2.groupby("interface", observed=True)["ct"]
    .agg(mean="mean", sd=lambda s: s.std(ddof=1), count="size")
    .reset_index()
)
ctSummary2["se"] = ctSummary2["sd"] / np.sqrt(ctSummary2["count"])
print("\nctSummary2:\n", ctSummary2)

# ---------------------------------------
# 2.4 ANOVA: effect of interface on ct (within-subjects)
# ---------------------------------------

ct_anova2 = pg.rm_anova(data=ctData2, dv="ct", within="interface", subject="id", detailed=True, effsize="np2")
print("\nRepeated-measures ANOVA (4 conditions):\n", ct_anova2)

# ---------------------------------------
# 2.5 Followup pairwise comparisons
# ---------------------------------------
# Pairwise t-tests with/without correction (Holm/Bonferroni)
pair_none = pg.pairwise_ttests(data=ctData2, dv="ct", within="interface", subject="id",
                               padjust="none", effsize="hedges")
pair_bonf = pg.pairwise_ttests(data=ctData2, dv="ct", within="interface", subject="id",
                               padjust="bonf", effsize="hedges")
pair_holm = pg.pairwise_ttests(data=ctData2, dv="ct", within="interface", subject="id",
                               padjust="holm", effsize="hedges")
print("\nPairwise (none):\n", pair_none)
print("\nPairwise (bonf):\n", pair_bonf)
print("\nPairwise (holm):\n", pair_holm)

# ========================================
# 2.6 Simple plot of the data
# ========================================

plt.figure()
plt.bar(ctSummary2["interface"].astype(str), ctSummary2["mean"])
plt.errorbar(
    x=np.arange(len(ctSummary2)),
    y=ctSummary2["mean"],
    yerr=ctSummary2["se"],
    fmt="none",
    capsize=6,
)
plt.xlabel("Interface")
plt.ylabel("Completion Time (sec)")
plt.title("CT by Interface (4 conditions)")
plt.savefig("ct-by-interface-4conds.png")
plt.close()


# ========================================
# Example 3: two factors (device, task); DV = completion time
# Within-subjects on both factors
# ========================================

# ---------------------------------------
# 3.1 Read the data
# ---------------------------------------

ctData3 = pd.read_csv("two-factor.log", sep="\t")
print(ctData3.head())
print(ctData3.columns.tolist())

# ---------------------------------------
# 3.2 Check the data and reformat if needed
# ---------------------------------------

precis(ctData3, "ctData3 (raw)")
for col in ["id", "device", "task"]:
    ctData3[col] = ctData3[col].astype("category")
precis(ctData3, "ctData3 (factored)")

ez_design(ctData3, x="device", y="id")
ez_design(ctData3, x="task",   y="id")

# ---------------------------------------
# 3.3 Summary stats by device and task
# ---------------------------------------

ctSummary3 = (
    ctData3.groupby(["device", "task"], observed=True)["ct"]
    .agg(mean="mean", sd=lambda s: s.std(ddof=1), count="size")
    .reset_index()
)
ctSummary3["se"] = ctSummary3["sd"] / np.sqrt(ctSummary3["count"])
print("\nctSummary3:\n", ctSummary3)

# ---------------------------------------
# 3.4 Two-way within-subjects ANOVA (device x task)
# ---------------------------------------
# pingouin accepts a list for within factors
ct_anova3 = pg.rm_anova(data=ctData3, dv="ct", within=["device", "task"], subject="id",
                        detailed=True, effsize="np2")
print("\nRM-ANOVA (device x task):\n", ct_anova3)

# ---------------------------------------
# 3.5 Followup pairwise (only for factor that showed a main effect)
# ---------------------------------------
# Example: follow-ups on device
pair_dev = pg.pairwise_ttests(data=ctData3, dv="ct", within="device", subject="id",
                              padjust="holm", effsize="hedges")
print("\nPairwise device (Holm):\n", pair_dev)

# ========================================
# 3.6 Plot (grouped bars with error bars)
# ========================================

# Prepare pivot for plotting
plot3 = ctSummary3.pivot(index="device", columns="task", values="mean")
order_device = [str(l) for l in ctSummary3["device"].cat.categories] if hasattr(ctSummary3["device"], "cat") else plot3.index

plt.figure()
width = 0.35
x = np.arange(len(order_device))
tasks = list(plot3.columns)

for i, t in enumerate(tasks):
    means = [ctSummary3[(ctSummary3["device"] == d) & (ctSummary3["task"] == t)]["mean"].values[0]
             for d in order_device]
    ses =   [ctSummary3[(ctSummary3["device"] == d) & (ctSummary3["task"] == t)]["se"].values[0]
             for d in order_device]
    plt.bar(x + i*width - width/2, means, width=width)
    plt.errorbar(x + i*width - width/2, means, yerr=ses, fmt="none", capsize=6)

plt.xticks(x, order_device)
plt.xlabel("Device")
plt.ylabel("Completion Time (sec)")
plt.title("CT by Device and Task (mean ± SE)")
plt.legend(tasks, title="Task", loc="upper right")
plt.ylim(bottom=0)
plt.savefig("ct-by-device-and-task.png")
plt.close()


# ========================================
# Example 4: Questionnaire data (TLX)
# ========================================

# ---------------------------------------
# 4.1 Read the data
# ---------------------------------------

tlxRaw = pd.read_csv("TLX-example-3.txt", sep="\t")
print(tlxRaw.head())

# ---------------------------------------
# 4.2 Check / reformat
# ---------------------------------------

tlxRaw["id"] = tlxRaw["id"].astype("category")
tlxRaw["ui"] = tlxRaw["ui"].astype("category")

precis(tlxRaw, "tlxRaw")
ez_design(tlxRaw, x="ui", y="id")

# Tidy: gather TLX questions into long format
id_vars = ["id", "ui"]
value_vars = [c for c in tlxRaw.columns if c not in id_vars]
tlxData = tlxRaw.melt(id_vars=id_vars, value_vars=value_vars, var_name="tlxQuestion", value_name="score")
print(tlxData.head())

# ---------------------------------------
# 4.3 Summary stats for each ui and question
# ---------------------------------------

tlxSummary = (
    tlxData.groupby(["ui", "tlxQuestion"], observed=True)["score"]
    .agg(
        median=lambda s: np.median(s.dropna()) - 1,
        mean=lambda s: s.dropna().mean() - 1,
        sd=lambda s: s.dropna().std(ddof=1),
        count="size",
    )
    .reset_index()
)
tlxSummary["se"] = tlxSummary["sd"] / np.sqrt(tlxSummary["count"])
print("\ntlxSummary:\n", tlxSummary.head())

# ---------------------------------------
# 4.4 Friedman tests (per-question) and Wilcoxon follow-ups
# ---------------------------------------
# For each DV (question), Friedman test across UIs within participants

def friedman_by_question(df_long, question):
    sub = df_long[df_long["tlxQuestion"] == question]
    # Pivot to shape (subjects x conditions)
    wide = sub.pivot(index="id", columns="ui", values="score")
    wide = wide.dropna(axis=0)  # complete cases
    stat, p = st.friedmanchisquare(*[wide[c] for c in wide.columns])
    return {"question": question, "stat": stat, "p": p, "cols": list(wide.columns)}

friedman_results = [friedman_by_question(tlxData, q) for q in tlxData["tlxQuestion"].unique()]
print("\nFriedman tests:")
for fr in friedman_results:
    print(fr)

# Example Wilcoxon follow-up (Gestures vs Menus) for one DV
def paired_wilcoxon_between_uis(df_long, question, ui_a, ui_b):
    sub = df_long[df_long["tlxQuestion"] == question]
    wide = sub.pivot(index="id", columns="ui", values="score")
    wide = wide.dropna(axis=0)
    if ui_a in wide.columns and ui_b in wide.columns and len(wide) > 0:
        stat, p = st.wilcoxon(wide[ui_a], wide[ui_b], zero_method='wilcox', alternative='two-sided')
        return {"question": question, "pair": (ui_a, ui_b), "n": len(wide), "stat": stat, "p": p}
    return {"question": question, "pair": (ui_a, ui_b), "n": 0, "stat": np.nan, "p": np.nan}

example_followups = [
    paired_wilcoxon_between_uis(tlxData, "mental",  "Gestures", "Menus"),
    paired_wilcoxon_between_uis(tlxData, "physical","Gestures", "Menus"),
]
print("\nWilcoxon follow-ups (examples):\n", example_followups)

# ---------------------------------------
# 4.5 Chart of means and s.e. for TLX
# ---------------------------------------

# Order + Labels to mimic your ggplot scale choices
y_ticks = [0, 2, 4, 6]
y_ticklabels = ["1 (least)", "3", "5", "7 (most)"]
x_order = ["mental", "physical", "rushed", "success", "work", "annoyed"]
x_labels = ["Mental\nEffort", "Physical\nEffort", "Rushed/\nHurried",
            "Perceived\nSuccess", "Hard Work\nRequired", "Annoyance/\nFrustration"]

# We’ll plot grouped bars per question with one bar per UI
uis = list(tlxSummary["ui"].astype(str).unique())
idx = pd.MultiIndex.from_product([x_order, uis], names=["tlxQuestion", "ui"])
plot_df = tlxSummary.set_index(["tlxQuestion", "ui"]).reindex(idx).reset_index()

# Compute bar positions
q_positions = np.arange(len(x_order))
width = 0.7
group_width = width
bar_w = group_width / max(1, len(uis))
offsets = np.linspace(-group_width/2 + bar_w/2, group_width/2 - bar_w/2, len(uis))

plt.figure(figsize=(10, 5))
for i, ui in enumerate(uis):
    sub = plot_df[plot_df["ui"] == ui]
    means = sub["mean"].values
    ses   = sub["se"].values
    plt.bar(q_positions + offsets[i], means, width=bar_w, label=ui)
    plt.errorbar(q_positions + offsets[i], means, yerr=ses, fmt="none", capsize=4)

plt.xticks(q_positions, x_labels)
plt.yticks(y_ticks, y_ticklabels)
plt.xlabel("NASA TLX Question")
plt.ylabel("Mean Score")
plt.legend(title=None, loc="upper center", ncol=len(uis))
plt.title("TLX Means by UI (±SE)")
plt.savefig("tlx-1.png")
plt.close()

# ---------------------------------------
# 4.6 Aligned Rank Transform for 2-factor analysis of TLX
# ---------------------------------------
# Python has no widely used ART equivalent; easiest is to call R's ARTool via rpy2.

def art_anova_via_R(df_long, question, formula="score ~ ui + Error(id)"):
    if not R_AVAILABLE:
        print("ART skipped: rpy2/R not available.")
        return None
    r = ro.r
    r('library(ARTool)')
    sub = df_long[df_long["tlxQuestion"] == question][["id", "ui", "score"]].copy()
    # Convert to R data.frame
    rdf = pandas2ri.py2rpy(sub)
    r.assign("tlxSub", rdf)
    r.assign("fstr", formula)
    r("tlxSub$id <- as.factor(tlxSub$id); tlxSub$ui <- as.factor(tlxSub$ui)")
    r("artResult <- art(as.formula(fstr), data=tlxSub)")
    # Show model summary + ANOVA + contrasts
    print(f"\n--- ART ({question}) summary ---")
    print(r("summary(artResult)"))
    print("\n--- ART ANOVA ---")
    print(r("anova(artResult)"))
    print("\n--- ART contrasts (ui) ---")
    print(r('art.con(artResult, "ui")'))

# Run ART for all TLX questions
for name in x_order:
    art_anova_via_R(tlxData, question=name)

# ===========================================================================
# Bootstrap test (example)
# ===========================================================================

# Example: bootstrap the mean of sepal_length in iris
# (Assumes you have an iris file; otherwise, replace with your own data/column)

def bootstrap_mean(x: np.ndarray, R=1000, random_state=42):
    rng = np.random.default_rng(random_state)
    n = len(x)
    boots = np.array([rng.choice(x, size=n, replace=True).mean() for _ in range(R)])
    return {
        "mean": x.mean(),
        "boot_mean": boots.mean(),
        "boot_se": boots.std(ddof=1),
        "ci_95": np.percentile(boots, [2.5, 97.5]),
        "samples": boots,
    }

# Example usage (uncomment and point to your data):
# iris = pd.read_csv("iris.csv")
# res = bootstrap_mean(iris["sepal_length"].values, R=1000)
# print("Bootstrap mean:", res["boot_mean"], "SE:", res["boot_se"], "95% CI:", res["ci_95"])
