from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.models.transaction import Transaction, TransactionType

def get_dashboard_summary(db: Session):
    # I'm starting off with a base query here that explicitly excludes soft-deleted transactions so that all the dashboard metrics are computed only on active data
    base_query = db.query(Transaction).filter(Transaction.is_deleted == False)
    income = base_query.filter(Transaction.type == TransactionType.income).with_entities(func.coalesce(func.sum(Transaction.amount), 0)).scalar()
    expense = base_query.filter(Transaction.type == TransactionType.expense).with_entities(func.coalesce(func.sum(Transaction.amount), 0)).scalar()
    
    # Category-wise totals : Here, we're doing Group By on both category and type (income/expense) so that we can easily distinguish, for example, income vs expense in the same category
    category_totals = base_query.with_entities(Transaction.category, Transaction.type, func.sum(Transaction.amount).label("total")).group_by(Transaction.category, Transaction.type).all()
    cats = [{"category": row.category, "type": row.type, "total": float(row.total)} for row in category_totals]
    
    # Recent activity : Here we're ordering by date DESC and then by id DESC to ensure that if there are multiple transactions on the same date, the most recent one appears first
    recent = base_query.order_by(Transaction.date.desc(), Transaction.id.desc()).limit(5).all()

    return {
        "total_income": float(income),
        "total_expenses": float(expense),
        "net_balance": float(income) - float(expense),
        "category_totals": cats,
        "recent_activity": [
            {
                "id": r.id, 
                "amount": float(r.amount), 
                "type": r.type, 
                "category": r.category, 
                "date": str(r.date)
            } for r in recent
        ]
    }

def get_trends(db: Session, period: str = "monthly"):
    # period can be monthly or weekly so we'll also dynamically adjust the grouping logic accordingly
    base_query = db.query(Transaction).filter(Transaction.is_deleted == False)
    if period == "monthly":
        # group by year and month
        group_fields = [extract('year', Transaction.date).label('year'), extract('month', Transaction.date).label('month'), Transaction.type]
    else:
        # group by year and week; this is likely more useful for a trend analysis on shorter time periods.
        group_fields = [extract('year', Transaction.date).label('year'), extract('week', Transaction.date).label('week'), Transaction.type]
    trends = base_query.with_entities(*group_fields, func.sum(Transaction.amount).label("total")).group_by(*group_fields).order_by(group_fields[0], group_fields[1]).all()
    result = []
    for row in trends:
        # row structure here would be (year, month/week, type, total)
        obj = {"year": int(row[0]), period: int(row[1]), "type": row[2], "total": float(row[3])}
        result.append(obj)    
    return result