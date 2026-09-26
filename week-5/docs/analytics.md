## Analytics Dashboard

The analytics section of the owner dashboard, built from the AnalyticsSection component and its useAnalytics hook, gives an owner a read on how the business is doing without needing a separate reporting tool. It surfaces revenue charts, which services are performing best, which days of the week are busiest, and what fraction of scheduled appointments are actually completed.

All of these figures are computed client-side, directly from the appointment data already sitting in Firestore -- there's no separate analytics backend, no scheduled job aggregating numbers overnight, and no third-party analytics service involved. Every chart reflects a live query over the same appointments collection everything else in the app reads from.

The dashboard lets an owner change the time window these figures cover, with three built-in options: This Week, This Month, and This Year, so an owner can check today's momentum or step back and look at longer-term trends using the exact same charts.
