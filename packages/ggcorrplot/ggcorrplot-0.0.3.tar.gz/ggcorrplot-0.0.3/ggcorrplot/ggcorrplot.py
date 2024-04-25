# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import plotnine as pn
import scipy.stats as st
from scipy.cluster import hierarchy
from scipy.spatial.distance import squareform

def get_melt(X):
    """
    """
    if not isinstance(X,pd.DataFrame):
            raise TypeError(
            f"{type(X)} is not supported. Please convert to a DataFrame with "
            "pd.DataFrame. For more information see: "
            "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html")
    return X.stack().rename_axis(('Var1', 'Var2')).reset_index(name='value')

def hc_cormat_order(cormat, method='complete'):
    """
    """
    if not isinstance(cormat,pd.DataFrame):
            raise TypeError(
            f"{type(cormat)} is not supported. Please convert to a DataFrame with "
            "pd.DataFrame. For more information see: "
            "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html")
    
    X = (1-cormat)/2
    Z = hierarchy.linkage(squareform(X),method=method, metric="euclidean")
    order = hierarchy.leaves_list(Z)
    return dict({"order":order,"height":Z[:,2],"method":method,
                "merge":Z[:,:2],"n_obs":Z[:,3],"data":cormat})

def match_arg(x, lst):
    return [el for el in lst if x in el][0]

def no_panel():
    return pn.theme(
        axis_title_x=pn.element_blank(),
        axis_title_y=pn.element_blank()
    )

def remove_diag(cormat):
    """
    
    
    """
    if cormat is None:
        return cormat
    
    if not isinstance(cormat,pd.DataFrame):
            raise TypeError(
            f"{type(cormat)} is not supported. Please convert to a DataFrame with "
            "pd.DataFrame. For more information see: "
            "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html")
    
    np.fill_diagonal(cormat.values, np.nan)
    return cormat

def get_upper_tri(cormat,show_diag=False):
    """
    
    """
    if cormat is None:
        return cormat
    
    if not isinstance(cormat,pd.DataFrame):
            raise TypeError(
            f"{type(cormat)} is not supported. Please convert to a DataFrame with "
            "pd.DataFrame. For more information see: "
            "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html")
    
    cormat = pd.DataFrame(np.triu(cormat),index=cormat.index,columns=cormat.columns)
    cormat.values[np.tril_indices(cormat.shape[0], -1)] = np.nan
    if not show_diag:
        np.fill_diagonal(cormat.values,np.nan)
    return cormat

def get_lower_tri(cormat,show_diag=False):
    """
    
    
    """
    if cormat is None:
        return cormat
    
    if not isinstance(cormat,pd.DataFrame):
            raise TypeError(
            f"{type(cormat)} is not supported. Please convert to a DataFrame with "
            "pd.DataFrame. For more information see: "
            "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html")
    
    cormat = pd.DataFrame(np.tril(cormat),index=cormat.index,columns=cormat.columns)
    cormat.values[np.triu_indices(cormat.shape[0], 1)] = np.nan
    if not show_diag:
        np.fill_diagonal(cormat.values,np.nan)
    return cormat

def cor_pmat(X,**kwargs):
    """
    Compute a correlation matrix p-values
    -------------------------------------

    Parameters
    ----------
    X : pandas dataframe of shape (n_rows, n_columns)

    **kwargs : other arguments to be passed to the function scipy.stats.pearsonr (see https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html)

    Return
    ------
    p_mat : pandas dataframe of shape (n_columns, n_columns), The p-value associated 

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    if not isinstance(X,pd.DataFrame):
            raise TypeError(
            f"{type(X)} is not supported. Please convert to a DataFrame with "
            "pd.DataFrame. For more information see: "
            "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html")
    
    y = np.array(X)
    n = y.shape[1]
    p_mat = np.zeros((n,n))
    np.fill_diagonal(p_mat,0)
    for i in np.arange(0,n-1):
        for j in np.arange(i+1,n):
            tmps = st.pearsonr(y[:,i],y[:,j],**kwargs)
            p_mat[i,j] = p_mat[j,i] = tmps[1]
    p_mat = pd.DataFrame(p_mat,index=X.columns,columns=X.columns)
    return p_mat

def ggcorrplot(X,
               matrix_type = "correlation",
               method = "square",
               type = "full",
               ggtheme = pn.theme_minimal(),
               title = None,
               show_legend = True,
               legend_title = "Corr",
               show_diag = None,
               colors = ["blue","white","red"],
               outline_color = "gray",
               hc_order = False,
               hc_method = "complete",
               label = False,
               label_color = "black",
               lab_size = 11,
               p_mat = None,
               sig_level=0.05,
               insig = "pch",
               pch = "x",
               pch_color = "black",
               pch_cex = 5,
               tl_cex = 12,
               tl_color = "black",
               tl_srt = 45,
               xtickslab_rotation = 45,
               digits = 2) -> pn:
    """
    Visualization of a correlation matrix using plotnine
    ----------------------------------------------------

    Description
    -----------

    A graphical display of a correlation matrix using plotnine
    
    Parameters
    ----------
    X : a pandas dataframe of shape (n_rows, n_columns) or (n_columns, n_columns)

    matrix_type : string, "correlation" (default) or "completed"

    method : string, the visualization method of correlation matrix to be used. Allowed values are "square" (default), "circle"

    type : string, "full" (default), "lower" or "upper" display

    ggtheme : plotnine function or theme object. Default value is "theme_minimal". Allowed values are the official plotnine themes including
                theme_gray, theme_bw, theme_minimal,, theme_classic, theme_void, ....

    title : string, title of the graph

    show_legend : bool, default = True, the legend is displayed

    legend_title : a string for the legend title. lower triangular, upper triangular or full matrix.

    show_diag : None or bool, whether display the correlation coefficients on the principal diagonal. If None, the default is to show diagonal
                correlation for type = "full" and to remove it when type is one of "upper" or "lower".
    
    colors : a list/tuple of 3 colors for low, mid and high correlation values

    outline_color : the outline color of square or circle. Default value is "gray".

    hc_order : bool, default = False. If True, correlation matrix will be hc_ordered using scipy.cluster.hierarchy.linkage function.

    hc_method : the agglomeration method to be used in scipy.cluster.hierarchy.linkage (see https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html#scipy.cluster.hierarchy.linkage)

    label : bool, default = False. If True, add correlation coefficient on the plot.

    label_color : size and color to be used for the correlation coefficients labels

    lab_size : used when lab = True

    p_mat : pandas dataframe of pvalue. If None, arguments sig_level, insig, pch, pch_col, pch_ces is invalid.

    sig_level : significant level, if the p-value in p_mat is bigger than sig_level, then the corresponding correlation coefficient is regarded as insignificant.

    insig : string, specialized insignificant correlation coefficients, "pch" (default), "blank". If "blank" wipe away the corresponding glyphs; 
            if "pch", add characters (see pch for details) on corresponding glyphs
        
    pch : add character on the glyphs of insignificant correlation coefficients (only valid when insig is "pch"). Default value is 'x'.

    pch_color, pch_cex : the color and the cex (size) of pch (only valid when insig is "pch")

    tl_cex, tl_color, tl_srt : the size, the color and the string rotation of text label (variable names)

    digits : Decides the number of decimal digits to be displayed (defaut = 2)

    Return
    ------
    a plotnine graph

    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE duverierdjifack@gmail.com
    """
    
    # Check if x is a pandas dataframe
    if not isinstance(X,pd.DataFrame):
            raise TypeError(
            f"{type(X)} is not supported. Please convert to a DataFrame with "
            "pd.DataFrame. For more information see: "
            "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html")
    
    # Check if matrix_type not in ["completed","correlation"]
    if not isinstance(matrix_type,str):
        raise TypeError("'matrix_type' should be a string")
    elif matrix_type not in ["completed","correlation"]:
        raise ValueError("'matrix_type' should be one of 'completed', 'correlation'")

    if p_mat is not None:
        # Check if p_mat is a pandas dataframe
        if not isinstance(p_mat,pd.DataFrame):
            raise TypeError(
            f"{type(p_mat)} is not supported. Please convert to a DataFrame with "
            "pd.DataFrame. For more information see: "
            "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html")

    # Check if type in ["full", "lower", "upper"]
    if not isinstance(type,str):
        raise TypeError("'type' should be a string")
    elif type not in ["full","lower","upper"]:
        raise ValueError("'type' should be one of 'full','lower', 'upper'")
    
    # Check if method in ["square","circle"]
    if not isinstance(method,str):
        raise TypeError("'method' sould be a string")
    elif method not in ["square","circle"]:
        raise ValueError("'method' should be one of 'square', 'circle'")
    
    # Check if insig in ["pch", "blank"]
    if not isinstance(insig,str):
        raise TypeError("'insig' should be a string")
    elif insig not in ["pch","blank"]:
        raise ValueError("'insig' should be one of 'pch', 'blank'")

    if show_diag is None:
        if type == "full":
            show_diag = True
        else:
            show_diag = False
    
    # Compute correlation matrix
    if matrix_type == "completed":
        corr = X.corr(method="pearson").round(decimals=digits)
    elif matrix_type == "correlation":
        corr = X.round(decimals=digits)

    if hc_order:
        ord = hc_cormat_order(corr,method=hc_method)["order"]
        corr = corr.iloc[ord,ord]
        if p_mat is not None:
            p_mat = p_mat.iloc[ord,ord]
            p_mat = p_mat.round(decimals=digits)

    if not show_diag:
        corr = remove_diag(corr)
        if p_mat is not None:
            p_mat = remove_diag(p_mat)
    
    # Get lower or upper triangle
    if type == "lower":
        corr = get_lower_tri(corr,show_diag)
        if p_mat is not None:
            p_mat = get_lower_tri(p_mat,show_diag)
    elif type == "upper":
        corr = get_upper_tri(corr,show_diag)
        if p_mat is not None:
            p_mat = get_upper_tri(corr,show_diag)
    
    # Melt corr and p_mat
    corr.columns = pd.Categorical(corr.columns,categories=corr.columns)
    corr.index = pd.Categorical(corr.columns,categories=corr.columns)
    corr = get_melt(corr)

    if p_mat is not None:
        p_mat = get_melt(p_mat)
        corr["coef"] = corr["value"]
        corr["pvalue"] = p_mat["value"]
        corr["signif"] = np.where(p_mat["value"] <= sig_level,1,0)
        p_mat = p_mat.query('value > @sig_level')
        if insig == "blank":
            corr["value"] = corr["value"]*corr["signif"]

    corr["abs_corr"] = 10*np.abs(corr["value"]) 

    p = pn.ggplot(corr,pn.aes(x="Var1",y="Var2",fill="value"))
    
    # Modification based on method
    if method == "square":
        p = p + pn.geom_tile(color=outline_color)
    elif method == "circle":
        p = p+pn.geom_point(pn.aes(size="abs_corr"),color=outline_color,shape="o")+pn.scale_size_continuous(range=(4,10))+pn.guides(size=None)
    
    # Adding colors
    p = p + pn.scale_fill_gradient2(low = colors[0],high = colors[2],mid = colors[1],midpoint = 0,limits = [-1,1],name = legend_title)

    # depending on the class of the object, add the specified theme
    p = p + ggtheme

    p =p+pn.theme(axis_text_x=pn.element_text(angle=tl_srt,va="center",size=tl_cex,ha="center",color=tl_color),
                  axis_text_y=pn.element_text(size=tl_cex)) + pn.coord_fixed()

    # Correlation label
    corr_label = corr["value"].round(digits)

    if p_mat is not None and insig == "blank":
        ns = corr["pvalue"] > sig_level
        if sum(ns) > 0:
            corr_label[ns] = " "
    
    # matrix cell labels
    if label:
        p = p + pn.geom_text(mapping=pn.aes(x="Var1",y="Var2"),label = corr_label,color = label_color,size=lab_size)
    
    # matrix cell 
    if p_mat is not None and insig == "pch":
        p = p + pn.geom_point(data = p_mat,mapping = pn.aes(x = "Var1",y = "Var2"),shape = pch,size=pch_cex,color= pch_color)
    
    if title is not None:
        p = p + pn.ggtitle(title=title)
    
    # Removing legend
    if not show_legend:
        p =p+pn.theme(legend_position=None)
    
    # Removing panel
    p = p + no_panel()

    if xtickslab_rotation > 5:
        ha = "right"
    if xtickslab_rotation == 90:
        ha = "center"
    # Rotation
    p = p + pn.theme(axis_text_x = pn.element_text(rotation = xtickslab_rotation,ha=ha))

    return p




    
    
    
    






