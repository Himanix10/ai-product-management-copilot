from backend.database.db import (
    fetch_customer_feedback_db,
    insert_customer_feedback_db,
    fetch_pain_points_db,
    save_initiative_db,
    fetch_initiatives_db
)

class DBTools:
    @staticmethod
    def get_feedback_records(category="All", search=""):
        return fetch_customer_feedback_db(category, search)

    @staticmethod
    def add_feedback_record(source, user_type, text, category):
        insert_customer_feedback_db(source, user_type, text, category)

    @staticmethod
    def get_pain_points(severity="All", search=""):
        return fetch_pain_points_db(severity, search)

    @staticmethod
    def add_initiative(title, reach, impact, confidence, effort, score, status="Planned"):
        save_initiative_db(title, reach, impact, confidence, effort, score, status)

    @staticmethod
    def get_initiatives():
        return fetch_initiatives_db()