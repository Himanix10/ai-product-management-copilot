from backend.database.db import DatabaseManager


class AnalyticsTools:

    @staticmethod
    def get_workspace_kpis():

        db_mgr = DatabaseManager()
        conn = db_mgr.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT COUNT(*) FROM feedback"
            )
            feedback_count = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM pain_points"
            )
            pain_points_count = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM initiatives"
            )
            initiatives_count = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM prds"
            )
            prds_count = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM roadmap
                WHERE status = 'In Progress'
                """
            )
            active_roadmap_items = cursor.fetchone()[0]

            return {
                "voc_feedback_volume": feedback_count,
                "active_pain_points": pain_points_count,
                "scored_initiatives": initiatives_count,
                "approved_prds": prds_count,
                "active_roadmap_items": active_roadmap_items,
            }

        finally:
            conn.close()