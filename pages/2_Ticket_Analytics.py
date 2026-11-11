
import streamlit as st
import pandas as pd
import plotly.express as px

from src.database import get_all_tickets


def show_dashboard():
    st.title("IT Support Analytics Dashboard")
    st.caption("Monitor support tickets, priorities, workloads and resolution status.")

    # Retrieve actual records from SQLite
    tickets = get_all_tickets()

    if not tickets:
        st.info("No support tickets are available yet.")
        return

    df = pd.DataFrame(tickets)

    # Data preparation
    df["priority"] = df["priority"].astype(str).str.upper()
    df["status"] = df["status"].astype(str).str.upper()
    df["created_at"] = pd.to_datetime(
        df["created_at"], errors="coerce"
    )

    # Derive issue categories from issue descriptions
    def categorize_issue(issue):
        issue = str(issue).lower()

        if any(word in issue for word in ["wifi", "wi-fi", "internet", "network", "vpn"]):
            return "Network"
        elif any(word in issue for word in ["keyboard", "mouse", "laptop", "computer", "hardware"]):
            return "Hardware"
        elif any(word in issue for word in ["password", "login", "account", "access"]):
            return "Account Access"
        elif any(word in issue for word in ["outlook", "software", "application", "app", "crash"]):
            return "Software"
        elif any(word in issue for word in ["printer", "printing"]):
            return "Printer"
        else:
            return "Other"

    df["category"] = df["issue"].apply(categorize_issue)

    # Dashboard filters
    st.subheader("Ticket Filters")

    col1, col2 = st.columns(2)

    with col1:
        selected_status = st.multiselect(
            "Filter by Status",
            sorted(df["status"].dropna().unique()),
            default=sorted(df["status"].dropna().unique())
        )

    with col2:
        selected_priority = st.multiselect(
            "Filter by Priority",
            ["HIGH", "MEDIUM", "LOW"],
            default=sorted(df["priority"].dropna().unique())
        )

    filtered_df = df[
        df["status"].isin(selected_status)
        & df["priority"].isin(selected_priority)
    ].copy()

    st.divider()

    # Key Performance Indicators
    st.subheader("Key Performance Indicators")

    total = len(filtered_df)
    open_count = int((filtered_df["status"] == "OPEN").sum())
    closed_count = int((filtered_df["status"] == "CLOSED").sum())
    closure_rate = (closed_count / total * 100) if total else 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Tickets", total)
    c2.metric("Open Tickets", open_count)
    c3.metric("Closed Tickets", closed_count)
    c4.metric("Closure Rate", f"{closure_rate:.1f}%")

    st.divider()

    if filtered_df.empty:
        st.warning("No tickets match the selected filters.")
        return

    # Priority and status analysis
    st.subheader("Ticket Distribution")

    left, right = st.columns(2)

    with left:
        priority_data = (
            filtered_df["priority"]
            .value_counts()
            .reindex(["HIGH", "MEDIUM", "LOW"], fill_value=0)
            .rename_axis("Priority")
            .reset_index(name="Tickets")
        )

        fig_priority = px.bar(
            priority_data,
            x="Priority",
            y="Tickets",
            color="Priority",
            title="Tickets by Priority",
            text="Tickets",
            color_discrete_map={
                "HIGH": "#ef4444",
                "MEDIUM": "#f97316",
                "LOW": "#22c55e"
            }
        )
        st.plotly_chart(fig_priority, use_container_width=True)

    with right:
        status_data = (
            filtered_df["status"]
            .value_counts()
            .rename_axis("Status")
            .reset_index(name="Tickets")
        )

        fig_status = px.pie(
            status_data,
            names="Status",
            values="Tickets",
            title="Open vs Closed Tickets",
            hole=0.45
        )
        st.plotly_chart(fig_status, use_container_width=True)

    # Issue category analysis
    st.subheader("Issue Category Analysis")

    category_data = (
        filtered_df["category"]
        .value_counts()
        .rename_axis("Category")
        .reset_index(name="Tickets")
    )

    fig_category = px.bar(
        category_data,
        x="Category",
        y="Tickets",
        title="Tickets by Issue Category",
        text="Tickets",
        color="Tickets"
    )
    st.plotly_chart(fig_category, use_container_width=True)

    # Ticket creation trend
    st.subheader("Ticket Creation Trend")

    trend_df = filtered_df.dropna(subset=["created_at"]).copy()

    if not trend_df.empty:
        trend_df["Date"] = trend_df["created_at"].dt.date

        trend_data = (
            trend_df.groupby("Date")
            .size()
            .reset_index(name="Tickets Created")
        )

        fig_trend = px.line(
            trend_data,
            x="Date",
            y="Tickets Created",
            markers=True,
            title="Daily Ticket Creation"
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    # Detailed ticket records
    st.subheader("Ticket Records")

    display_df = filtered_df[
        [
            "ticket_id",
            "user_name",
            "issue",
            "category",
            "priority",
            "status",
            "created_at"
        ]
    ].copy()

    display_df.columns = [
        "Ticket ID",
        "User",
        "Issue",
        "Category",
        "Priority",
        "Status",
        "Created At"
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    # Export filtered records
    csv_data = display_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Ticket Report (CSV)",
        data=csv_data,
        file_name="it_support_ticket_report.csv",
        mime="text/csv"
    )

show_dashboard()
