#coding:utf-8
__author__ = 'Johnny'

from scapp import db

# 资产负债表-其它经营资产
class SC_Assets_Other_Operate_Assets(db.Model):
    '''
    资产负债表-其它经营资产
    '''
    __tablename__ = 'sc_assets_other_operate_assets'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    project=db.Column(db.String(32))#项目名称
    describe=db.Column(db.String(16))#描述
    amount=db.Column(db.String(16))#金额

    def __init__(self,loan_apply_id,project,describe,amount):
        self.loan_apply_id = loan_apply_id
        self.project = project
        self.describe = describe
        self.amount = amount

    def add(self):
        db.session.add(self)