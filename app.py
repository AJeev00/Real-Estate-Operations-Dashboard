import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="EstateOps | Project Control", page_icon="🏗️", layout="wide")
st.title("EstateOps")
st.caption("Real Estate Construction Operations | Portfolio demonstration using simulated data")
DATA = Path(__file__).parent / "data" / "projects.csv"
df = pd.read_csv(DATA)
st.sidebar.header("Portfolio filters")
projects = ["All"] + sorted(df["project"].unique().tolist())
selected = st.sidebar.selectbox("Project", projects)
status_filter = st.sidebar.multiselect("Status", sorted(df.status.unique()), default=sorted(df.status.unique()))
view = df.copy()
if selected != "All": view = view[view.project == selected]
view = view[view.status.isin(status_filter)]
if view.empty:
    st.warning("No records match these filters.")
    st.stop()
planned = view.planned_progress.mean()
actual = view.actual_progress.mean()
budget = view.budget_inr.sum()
spent = view.spent_inr.sum()
c1,c2,c3,c4 = st.columns(4)
c1.metric("Average physical progress", f"{actual:.1f}%", f"{actual-planned:+.1f} pp vs plan")
c2.metric("Total approved budget", f"₹{budget/1e7:.2f} Cr")
c3.metric("Budget utilised", f"{spent/budget*100:.1f}%", f"₹{(budget-spent)/1e7:.2f} Cr remaining")
c4.metric("Active work packages", f"{len(view)}")
left,right=st.columns(2)
with left:
    st.subheader("Planned vs actual progress")
    long=view.melt(id_vars="project",value_vars=["planned_progress","actual_progress"],var_name="measure",value_name="progress")
    st.plotly_chart(px.bar(long,x="project",y="progress",color="measure",barmode="group",labels={"progress":"Progress (%)","project":"Project","measure":"Measure"}),use_container_width=True)
with right:
    st.subheader("Budget utilisation by project")
    spend=view.groupby("project",as_index=False)[["budget_inr","spent_inr"]].sum()
    spend["utilisation_pct"]=spend.spent_inr/spend.budget_inr*100
    st.plotly_chart(px.bar(spend,x="project",y="utilisation_pct",color="utilisation_pct",labels={"utilisation_pct":"Budget utilised (%)"}),use_container_width=True)
st.subheader("Site performance register")
view["schedule_variance_pp"] = (view.actual_progress-view.planned_progress).round(1)
view["budget_utilisation_pct"]=(view.spent_inr/view.budget_inr*100).round(1)
st.dataframe(view[["project","work_package","status","planned_progress","actual_progress","schedule_variance_pp","budget_inr","spent_inr","budget_utilisation_pct","site_manager"]],use_container_width=True,hide_index=True)
st.subheader("Operational alerts")
alerts=[]
for _,r in view.iterrows():
    if r.actual_progress < r.planned_progress-8: alerts.append(f"🔴 {r.project} / {r.work_package}: progress is {r.planned_progress-r.actual_progress:.1f} percentage points behind plan.")
    if r.spent_inr/r.budget_inr > .85 and r.actual_progress < 75: alerts.append(f"🟠 {r.project} / {r.work_package}: over 85% of budget used while progress is below 75%.")
if alerts:
    for a in alerts: st.warning(a)
else: st.success("No threshold-based operational alerts in the selected view.")
st.download_button("Download filtered register (CSV)",view.to_csv(index=False).encode(), "operations_register.csv","text/csv")
st.info("Decision-support prototype only. Data is synthetic; alerts are configurable thresholds, not professional project controls advice.")
