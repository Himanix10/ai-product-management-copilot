from backend.database.db import DatabaseManager


class RetrievalTools:

    def search_documents(
        self,
        query: str
    ) -> str:

        db_mgr = DatabaseManager()
        conn = db_mgr.get_connection()

        try:
            q_lower = query.lower()
            clean_query = query.strip()
            search_term = f"%{clean_query}%"

            # Check intent keywords
            is_pain_point_query = any(k in q_lower for k in ["pain", "point", "cluster", "theme", "problem", "issue", "frustration"])
            is_feedback_query = any(k in q_lower for k in ["feedback", "voc", "customer", "user", "sentiment"])
            is_initiative_query = any(k in q_lower for k in ["initiative", "feature", "rice", "priorit"])
            is_prd_query = any(k in q_lower for k in ["prd", "requirement", "doc", "spec"])
            is_roadmap_query = any(k in q_lower for k in ["roadmap", "quarter", "milestone", "release", "plan"])
            is_metric_query = any(k in q_lower for k in ["metric", "kpi", "dau", "mau", "conversion"])
            is_general_query = any(k in q_lower for k in ["proceed", "next", "start", "guide", "help", "how", "what", "overview", "explain"])

            # -------------------------------------------------
            # PAIN POINTS
            # -------------------------------------------------
            pain_points_sql = """
                SELECT cluster_id, theme_name, category, description, feedback_count, priority_level, status
                FROM pain_points
                WHERE theme_name LIKE ? OR category LIKE ? OR description LIKE ?
                ORDER BY feedback_count DESC LIMIT 5
            """
            pain_points = conn.execute(pain_points_sql, (search_term, search_term, search_term)).fetchall()
            if not pain_points and (is_pain_point_query or is_general_query):
                pain_points = conn.execute(
                    "SELECT cluster_id, theme_name, category, description, feedback_count, priority_level, status FROM pain_points ORDER BY feedback_count DESC LIMIT 5"
                ).fetchall()

            # -------------------------------------------------
            # FEEDBACK
            # -------------------------------------------------
            feedbacks_sql = """
                SELECT feedback_text, theme, priority, sentiment
                FROM feedback
                WHERE feedback_text LIKE ? OR theme LIKE ?
                LIMIT 5
            """
            feedbacks = conn.execute(feedbacks_sql, (search_term, search_term)).fetchall()
            if not feedbacks and (is_feedback_query or is_general_query):
                feedbacks = conn.execute(
                    "SELECT feedback_text, theme, priority, sentiment FROM feedback LIMIT 5"
                ).fetchall()

            # -------------------------------------------------
            # INITIATIVES
            # -------------------------------------------------
            initiatives_sql = """
                SELECT feature_name, theme, rice_score, priority_level, status
                FROM initiatives
                WHERE feature_name LIKE ? OR theme LIKE ?
                ORDER BY rice_score DESC LIMIT 5
            """
            initiatives = conn.execute(initiatives_sql, (search_term, search_term)).fetchall()
            if not initiatives and (is_initiative_query or is_general_query):
                initiatives = conn.execute(
                    "SELECT feature_name, theme, rice_score, priority_level, status FROM initiatives ORDER BY rice_score DESC LIMIT 5"
                ).fetchall()

            # -------------------------------------------------
            # PRDs
            # -------------------------------------------------
            prds_sql = """
                SELECT title, problem_statement, status
                FROM prds
                WHERE title LIKE ? OR problem_statement LIKE ? OR user_personas LIKE ?
                LIMIT 5
            """
            prds = conn.execute(prds_sql, (search_term, search_term, search_term)).fetchall()
            if not prds and (is_prd_query or is_general_query):
                prds = conn.execute(
                    "SELECT title, problem_statement, status FROM prds LIMIT 5"
                ).fetchall()

            # -------------------------------------------------
            # ROADMAP
            # -------------------------------------------------
            roadmap_sql = """
                SELECT title, quarter, status, progress_percentage
                FROM roadmap
                WHERE title LIKE ? OR theme LIKE ? OR milestone LIKE ?
                LIMIT 5
            """
            roadmap = conn.execute(roadmap_sql, (search_term, search_term, search_term)).fetchall()
            if not roadmap and (is_roadmap_query or is_general_query):
                roadmap = conn.execute(
                    "SELECT title, quarter, status, progress_percentage FROM roadmap LIMIT 5"
                ).fetchall()

            # -------------------------------------------------
            # PRODUCT METRICS
            # -------------------------------------------------
            metrics_sql = """
                SELECT metric_name, category, metric_value, unit, trend, status
                FROM product_metrics
                WHERE metric_name LIKE ? OR category LIKE ?
                LIMIT 5
            """
            metrics = conn.execute(metrics_sql, (search_term, search_term)).fetchall()
            if not metrics and (is_metric_query or is_general_query):
                metrics = conn.execute(
                    "SELECT metric_name, category, metric_value, unit, trend, status FROM product_metrics LIMIT 5"
                ).fetchall()

        finally:
            conn.close()

        context_blocks = []

        if pain_points:
            context_blocks.append(
                "### 🔴 Customer Pain Points:\n"
                + "\n".join([
                    f"- **{row['theme_name']}** ({row['category']}): {row['description']} (Feedback Count: {row['feedback_count']}, Priority: {row['priority_level']}, Status: {row['status']})"
                    for row in pain_points
                ])
            )

        if feedbacks:
            context_blocks.append(
                "### 💬 Customer VOC Feedback:\n"
                + "\n".join([
                    f"- [{row['theme']}] \"{row['feedback_text']}\" (Priority: {row['priority']}, Sentiment: {row['sentiment']})"
                    for row in feedbacks
                ])
            )

        if initiatives:
            context_blocks.append(
                "### 🚀 Prioritized Feature Initiatives:\n"
                + "\n".join([
                    f"- **{row['feature_name']}** (Theme: {row['theme']}, RICE Score: {row['rice_score']}, Priority: {row['priority_level']}, Status: {row['status']})"
                    for row in initiatives
                ])
            )

        if prds:
            context_blocks.append(
                "### 📄 Product Requirement Documents (PRDs):\n"
                + "\n".join([
                    f"- **{row['title']}**: {row['problem_statement']} (Status: {row['status']})"
                    for row in prds
                ])
            )

        if roadmap:
            context_blocks.append(
                "### 🗓️ Roadmap Milestones:\n"
                + "\n".join([
                    f"- **{row['title']}** ({row['quarter']}, Status: {row['status']}, {row['progress_percentage']}% complete)"
                    for row in roadmap
                ])
            )

        if metrics:
            context_blocks.append(
                "### 📊 Key Product Metrics:\n"
                + "\n".join([
                    f"- **{row['metric_name']}** ({row['category']}): Value = {row['metric_value']} {row['unit']}, Trend = {row['trend']}, Status = {row['status']}"
                    for row in metrics
                ])
            )

        if not context_blocks:
            return (
                f"No specific database matches were found for '{query}'. "
                "The workspace active data includes Customer Feedback, Pain Point Clusters, Feature Initiatives, PRDs, and Roadmap schedules."
            )

        return "\n\n".join(context_blocks)