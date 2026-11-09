# Tab Navigation + Spaced Repetition

## Motivation
The current HomePage mixes course list, stats, and review reminders in one scrollable page, making it cluttered. Learning apps like 百词斩 use bottom tab navigation to separate concerns into dedicated modules.

## Design
4-tab bottom navigation bar:

| Tab | Icon | Content |
|---|---|---|
| 学习 | 📖 | Course list, continue learning, create course |
| 复习 | 🔄 | All pending/overdue reviews with SM-2 status |
| 统计 | 📊 | Learning stats, streaks, achievements, certificates |
| 我的 | 👤 | AI config, about, preferences |

## Architecture
- `HomePage.ets` → Tabs container (no longer has own content)
- `component/LearnTab.ets` → Extracted from HomePage course list
- `component/ReviewTab.ets` → Extracted from HomePage review section + enhanced
- `component/StatsTab.ets` → Wraps ProgressDashboardPage functionality
- `component/ProfileTab.ets` → Settings page (new)
