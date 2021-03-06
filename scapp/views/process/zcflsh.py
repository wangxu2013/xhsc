# coding:utf-8

import os

from flask import Module, session, request, render_template, redirect, url_for,flash
from flask.ext.login import current_user
import datetime

from scapp import db
from scapp.config import logger
from scapp.config import PER_PAGE

from scapp.models import SC_Loan_Apply
from scapp.models import SC_Co_Borrower
from scapp.models import SC_Guaranty
from scapp.models import SC_Guarantees
from scapp.models import View_Query_Loan

from scapp import app

from scapp.models import SC_Loan_Product

# 资产分类审核搜索
@app.route('/Process/zcflsh/zcflsh', methods=['GET'])
def zcflsh_search():
    loan_product = SC_Loan_Product.query.all()
    return render_template("Process/zcflsh/zcflsh_search.html",loan_product=loan_product)

# 资产分类审核
@app.route('/Process/zcflsh/zcflsh_search/<int:page>', methods=['GET','POST'])
def Process_zcflsh(page):
    customer_name = request.form['customer_name']
    loan_type = request.form['loan_type']
    classify = request.form['classify']
    sql = " 1=1"
    if loan_type != '0':
        sql = " and loan_type='"+loan_type+"'"
    if classify != '0':
        sql += " and classify="+classify
    if customer_name:
        sql += " and (company_customer_name like '%"+customer_name+"%' or individual_customer_name like '%"+customer_name+"%')"
    
    loan_apply = View_Query_Loan.query.filter(sql).paginate(page, per_page = PER_PAGE)
    
    loan_product = SC_Loan_Product.query.all()
    
    return render_template("Process/zcflsh/zcflsh.html",loan_apply=loan_apply,customer_name=customer_name,
    	loan_type=loan_type,classify=classify,loan_product=loan_product)

# 资产分类审核——审核资产分类
@app.route('/Process/zcflsh/check_zcfl/<int:loan_apply_id>', methods=['GET','POST'])
def check_zcfl(loan_apply_id):
    if request.method == 'GET':
        view_query_loan = View_Query_Loan.query.filter_by(loan_apply_id=loan_apply_id).first()
        co_borrower = SC_Co_Borrower.query.filter_by(loan_apply_id=loan_apply_id).all()
        guaranty = SC_Guaranty.query.filter_by(loan_apply_id=loan_apply_id).all()
        guarantees = SC_Guarantees.query.filter_by(loan_apply_id=loan_apply_id).all()
        
        loan_product = SC_Loan_Product.query.all()
        
        return render_template("Process/zcflsh/check_zcfl.html",view_query_loan=view_query_loan,
        	co_borrower=co_borrower,guaranty=guaranty,guarantees=guarantees,loan_product=loan_product)
    else:
        try:
            loan_apply = SC_Loan_Apply.query.filter_by(id=loan_apply_id).first()
            loan_apply.classify = request.form['classify']
            loan_apply.classify_dec = request.form['classify_dec']
            
            # 事务提交
            db.session.commit()
            # 消息闪现
            flash('保存成功','success')
        except:
            # 回滚
            db.session.rollback()
            logger.exception('exception')
            # 消息闪现
            flash('保存失败','error')
    
        return redirect('Process/zcflsh/zcflsh')