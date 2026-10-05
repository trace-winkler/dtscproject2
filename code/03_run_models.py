"""Step 3: multinomial logistic regression + decision tree.
Evaluation = leave-one-DRAFT-YEAR-out: each year takes a turn as the test set while the
models train on the other years, then results are pooled. Writes results to outputs/.
"""
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import GridSearchCV, GroupKFold, LeaveOneGroupOut
from sklearn.metrics import accuracy_score, f1_score, classification_report, ConfusionMatrixDisplay
from config import *

df = pd.read_csv(DATA / "model_data.csv")
hist_cols = [c for c in df.columns if c.startswith("hist_")]
FEATURES = RANK_COLS + ["pick", "win_pct"] + hist_cols
df["win_pct"] = df["win_pct"].fillna(df["win_pct"].median())
X, y, years = df[FEATURES], df["target"], df["draft_year"]
print(f"{len(df)} rows, draft years {sorted(years.unique())}, classes {sorted(y.unique())}")

def make_models(n_train_years):
    cv = GroupKFold(n_splits=min(5, n_train_years))
    return {
        "Baseline (most common)": DummyClassifier(strategy="most_frequent"),
        "Multinomial Logistic Regression": GridSearchCV(
            make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000)),
            {"logisticregression__C": [0.01, 0.1, 1, 10],
             "logisticregression__class_weight": [None, "balanced"]},
            cv=cv, scoring="accuracy"),
        "Decision Tree": GridSearchCV(
            DecisionTreeClassifier(random_state=42),
            {"max_depth": [2, 3, 4], "min_samples_leaf": [3, 5, 10],
             "class_weight": [None, "balanced"]},
            cv=cv, scoring="accuracy"),
    }

def fit(model, Xt, yt, gt):
    if isinstance(model, GridSearchCV):
        model.fit(Xt, yt, groups=gt)
    else:
        model.fit(Xt, yt)
    return model

def top3_hits(model, Xt, yt):
    est = model.best_estimator_ if isinstance(model, GridSearchCV) else model
    if not hasattr(est, "predict_proba") or isinstance(est, DummyClassifier):
        return None   # baseline top-3 is not meaningful
    p = est.predict_proba(Xt)
    top = est.classes_[np.argsort(-p, axis=1)[:, :3]]
    return np.array([t in row for t, row in zip(yt, top)])

# ---- Leave-one-year-out evaluation ----
preds = {name: np.empty(len(df), dtype=object) for name in make_models(2)}
top3 = {name: np.full(len(df), np.nan) for name in preds}
for tr, te in LeaveOneGroupOut().split(X, y, groups=years):
    models = make_models(years.iloc[tr].nunique())
    for name, m in models.items():
        fit(m, X.iloc[tr], y.iloc[tr], years.iloc[tr])
        preds[name][te] = m.predict(X.iloc[te])
        h = top3_hits(m, X.iloc[te], y.iloc[te])
        if h is not None:
            top3[name][te] = h

lines = []
for name in preds:
    p = pd.Series(preds[name], index=df.index)
    lines.append(f"\n=== {name} (pooled leave-one-year-out, n={len(df)}) ===")
    lines.append(f"Accuracy: {accuracy_score(y, p):.3f}")
    lines.append(f"Macro-F1: {f1_score(y, p, average='macro', zero_division=0):.3f}")
    if not np.isnan(top3[name]).all():
        lines.append(f"Top-3 accuracy: {np.nanmean(top3[name]):.3f}")
    by_year = (p == y).groupby(years).mean().round(3)
    lines.append("Accuracy by held-out draft year: " + ", ".join(f"{k}: {v}" for k, v in by_year.items()))
    lines.append(classification_report(y, p, zero_division=0))
    if not name.startswith("Baseline"):
        fig, ax = plt.subplots(figsize=(7, 6))
        ConfusionMatrixDisplay.from_predictions(y, p, ax=ax, xticks_rotation=45)
        ax.set_title(name); fig.tight_layout()
        tag = "logistic" if "Logistic" in name else "tree"
        fig.savefig(OUT / f"confusion_{tag}.png", dpi=150); plt.close(fig)

# ---- Final fits on ALL years, for coefficients and the tree diagram ----
final = make_models(years.nunique())
for name in ("Multinomial Logistic Regression", "Decision Tree"):
    fit(final[name], X, y, years)
    lines.append(f"\nFinal {name} best params (all data): {final[name].best_params_}")

lr = final["Multinomial Logistic Regression"].best_estimator_.named_steps["logisticregression"]
pd.DataFrame(lr.coef_, index=lr.classes_, columns=FEATURES).to_csv(OUT / "logistic_coefficients.csv")

tree = final["Decision Tree"].best_estimator_
fig, ax = plt.subplots(figsize=(22, 10))
plot_tree(tree, feature_names=FEATURES, class_names=list(tree.classes_), filled=True, fontsize=7, ax=ax)
fig.savefig(OUT / "decision_tree.png", dpi=150, bbox_inches="tight"); plt.close(fig)
pd.Series(tree.feature_importances_, index=FEATURES).sort_values(ascending=False)\
  .to_csv(OUT / "tree_feature_importance.csv", header=["importance"])

text = "\n".join(lines)
(OUT / "results.txt").write_text(text)
print(text)
print("\nSaved results, coefficients, importances and figures to outputs/")
