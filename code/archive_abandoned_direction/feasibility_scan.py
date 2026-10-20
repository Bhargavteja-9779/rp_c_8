"""Feasibility scan (Gate D): descriptive duplicate statistics for OpenML-CC18. NO model performance is computed here."""
import requests, json, sys, time, numpy as np, pandas as pd
from sklearn.datasets import fetch_openml
DATA_HOME="/tmp/oml_cache"
ids=[int(i) for i in requests.get("https://www.openml.org/api/v1/json/study/OpenML-CC18",timeout=60).json()["study"]["data"]["data_id"]]
rows=[]
for i in ids:
    try:
        t=time.time()
        b=fetch_openml(data_id=i,as_frame=True,parser="auto",data_home=DATA_HOME)
        X,y=b.data,b.target
        n,p=X.shape
        full=pd.concat([X,y.rename("__y__")],axis=1)
        dup_x=X.duplicated(keep=False).mean(); dup_xy=full.duplicated(keep=False).mean()
        gx=X.groupby(list(X.columns),dropna=False,observed=True).ngroup()
        nuniq=gx.nunique()
        # label-conflict: unique X with >1 label
        conf=full.groupby(gx.values)["__y__"].nunique().gt(1).sum()
        rows.append(dict(id=i,name=b.details["name"],n=n,p=p,n_classes=y.nunique(),n_unique_x=nuniq,frac_rows_in_dup_group=round(dup_x,4),
            frac_rows_exact_dupxy=round(dup_xy,4),dup_groups_label_conflict=int(conf),n_numeric=int(X.select_dtypes("number").shape[1]),sec=round(time.time()-t,1)))
        print(rows[-1],flush=True)
    except Exception as e:
        print("FAIL",i,repr(e)[:150],flush=True)
pd.DataFrame(rows).to_csv("/home/user/rp_c_8/research_design/feasibility_cc18_descriptives.csv",index=False)
