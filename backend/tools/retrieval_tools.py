from backend.database.db import DatabaseManager


class RetrievalTools:

    def search_documents(
        self,
        query: str
    ) -> str:

        db_mgr = DatabaseManager()
        conn = db_mgr.get_connection()

        try:

            search_term = f"%{query}%"

            # -------------------------------------------------
            # FEEDBACK
            # -------------------------------------------------

            feedbacks = conn.execute(
                """
                SELECT
                    feedback_text,
                    theme,
                    priority
                FROM feedback
                WHERE
                    feedback_text LIKE ?
                    OR theme LIKE ?
                LIMIT 5
                """,
                (
                    search_term,
                    search_term,
                ),
            ).fetchall()

            # -------------------------------------------------
            # INITIATIVES
            # -------------------------------------------------

            initiatives = conn.execute(
                """
                SELECT
                    feature_name,
                    rice_score,
                    status
                FROM initiatives
                WHERE
                    feature_name LIKE ?
                    OR theme LIKE ?
                ORDER BY rice_score DESC
                LIMIT 5
                """,
                (
                    search_term,
                    search_term,
                ),
            ).fetchall()

            # -------------------------------------------------
            # PRDs
            # -------------------------------------------------

            prds = conn.execute(
                """
                SELECT
                    title,
                    problem_statement,
                    status
                FROM prds
                WHERE
                    title LIKE ?
                    OR problem_statement LIKE ?
                    OR user_personas LIKE ?
                LIMIT 5
                """,
                (
                    search_term,
                    search_term,
                    search_term,
                ),
            ).fetchall()

            # -------------------------------------------------
            # ROADMAP
            # -------------------------------------------------

            roadmap = conn.execute(
                """
                SELECT
                    title,
                    quarter,
                    status,
                    progress_percentage
                FROM roadmap
                WHERE
                    title LIKE ?
                    OR theme LIKE ?
                    OR milestone LIKE ?
                LIMIT 5
                """,
                (
                    search_term,
                    search_term,
                    search_term,
                ),
            ).fetchall()

        finally:
            conn.close()

        context_blocks = []

        if feedbacks:

            context_blocks.append(
                "Matching VOC Feedback:\n"
                + "\n".join(
                    [
                        (
                            f"- [{row['theme']}] "
                            f"{row['feedback_text']} "
                            f"(Priority: "
                            f"{row['priority']})"
                        )
                        for row in feedbacks
                    ]
                )
            )

        if initiatives:

            context_blocks.append(
                "Matching Initiatives:\n"
                + "\n".join(
                    [
                        (
                            f"- {row['feature_name']} "
                            f"(RICE: {row['rice_score']}, "
                            f"Status: {row['status']})"
                        )
                        for row in initiatives
                    ]
                )
            )

        if prds:

            context_blocks.append(
                "Matching PRDs:\n"
                + "\n".join(
                    [
                        (
                            f"- {row['title']}: "
                            f"{row['problem_statement']} "
                            f"(Status: {row['status']})"
                        )
                        for row in prds
                    ]
                )
            )

        if roadmap:

            context_blocks.append(
                "Matching Roadmap Items:\n"
                + "\n".join(
                    [
                        (
                            f"- {row['title']} "
                            f"({row['quarter']}, "
                            f"{row['status']}, "
                            f"{row['progress_percentage']}% complete)"
                        )
                        for row in roadmap
                    ]
                )
            )

        if not context_blocks:

            return (
                f"No exact database matches were found "
                f"for '{query}'.\n\n"
                "The workspace contains VOC feedback, "
                "pain points, initiatives, PRDs and "
                "roadmap records."
            )

        return "\n\n".join(
            context_blocks
        )