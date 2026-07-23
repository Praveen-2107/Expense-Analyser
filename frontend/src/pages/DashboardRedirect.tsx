import { useEffect, useState } from 'react';

import { AnalyticsInsights } from '../components/analytics/AnalyticsInsights';
import { CategoryDistributionChart } from '../components/analytics/CategoryDistributionChart';
import { SpendingTrendChart } from '../components/analytics/SpendingTrendChart';
import { useAuth } from '../context/AuthContext';
import { fetchAIInsights } from '../services/aiService';

export function DashboardRedirect() {
  const { user, logout } = useAuth();

  const summaryCards = [
    { label: 'Monthly Income', value: '$8,450', delta: '+12.4%', tone: 'positive' },
    { label: 'Monthly Expenses', value: '$5,280', delta: '-3.1%', tone: 'neutral' },
    { label: 'Savings Rate', value: '37%', delta: '+5.8%', tone: 'positive' },
    { label: 'Active Budgets', value: '7', delta: '2 alerts', tone: 'warning' }
  ] as const;

  const categoryBreakdown = [
    { name: 'Housing', amount: '$1,920', percent: 34, color: 'bg-primary' },
    { name: 'Food & Dining', amount: '$1,120', percent: 20, color: 'bg-success' },
    { name: 'Transport', amount: '$760', percent: 14, color: 'bg-warning' },
    { name: 'Subscriptions', amount: '$420', percent: 8, color: 'bg-info' },
    { name: 'Others', amount: '$1,060', percent: 24, color: 'bg-secondary' }
  ] as const;

  const recentTransactions = [
    { title: 'Grocery Mart', category: 'Food & Dining', amount: '-$86.40', date: 'Today' },
    { title: 'Metro Card', category: 'Transport', amount: '-$42.00', date: 'Yesterday' },
    { title: 'Salary Deposit', category: 'Income', amount: '+$4,500.00', date: '2 days ago' },
    { title: 'Streaming Bundle', category: 'Subscriptions', amount: '-$18.99', date: '3 days ago' }
  ] as const;

  const [aiSummary, setAiSummary] = useState('Analyzing your financial activity...');
  const [aiInsights, setAiInsights] = useState<string[]>([
    'Loading AI insights for your latest spending data.',
    'This section will update automatically from the backend.',
    'If Gemini is unavailable, the app will use deterministic fallback insights.'
  ]);
  const [aiRecommendations, setAiRecommendations] = useState<string[]>([]);
  const [aiSource, setAiSource] = useState<'gemini' | 'fallback'>('fallback');

  const spendingTrend = [
    { month: 'Jan', amount: 4200 },
    { month: 'Feb', amount: 3800 },
    { month: 'Mar', amount: 5100 },
    { month: 'Apr', amount: 4700 },
    { month: 'May', amount: 6200 },
    { month: 'Jun', amount: 5600 }
  ];

  useEffect(() => {
    let isMounted = true;

    fetchAIInsights({ focus: 'spending trend analysis and saving recommendations' })
      .then((response) => {
        if (!isMounted) {
          return;
        }
        setAiSummary(response.summary);
        setAiInsights(response.insights);
        setAiRecommendations(response.recommendations);
        setAiSource(response.used_gemini ? 'gemini' : 'fallback');
      })
      .catch(() => {
        if (!isMounted) {
          return;
        }
        setAiSummary('Unable to load live AI insights right now.');
        setAiInsights([
          'The backend AI endpoint is unavailable at the moment.',
          'Review the spending and budget sections for manual analysis.',
          'Reconnect Gemini in the environment variables to enable generative insights.'
        ]);
        setAiRecommendations([
          'Verify the backend is running and authenticated.',
          'Set the Gemini API key in your environment when ready.',
          'Retry the dashboard after the AI service is available.'
        ]);
        setAiSource('fallback');
      });

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <main className="dashboard-shell min-vh-100 py-4 py-lg-5 px-3 px-lg-4">
      <section className="container-fluid dashboard-container">
        <div className="dashboard-header card border-0 shadow-sm rounded-4 mb-4 overflow-hidden">
          <div className="card-body p-4 p-lg-5 dashboard-hero">
            <div className="d-flex flex-column flex-xl-row justify-content-between gap-4">
              <div className="text-white">
                <p className="text-uppercase small fw-semibold mb-2 text-white-50">AI Expense Analyzer</p>
                <h1 className="display-6 fw-bold mb-3">Good to see you, {user?.fullName}</h1>
                <p className="lead mb-0 text-white-75 dashboard-subtitle">
                  Your finances are trending in the right direction. Review spending, adjust budgets, and let AI highlight
                  the patterns that matter.
                </p>
              </div>
              <div className="dashboard-actions d-flex flex-wrap gap-3 align-items-start">
                <button className="btn btn-light btn-lg fw-semibold" type="button">
                  Export Report
                </button>
                <button className="btn btn-outline-light btn-lg fw-semibold" type="button" onClick={logout}>
                  Logout
                </button>
              </div>
            </div>
          </div>
        </div>

        <div className="row g-4 mb-4">
          {summaryCards.map((card) => (
            <div className="col-12 col-md-6 col-xxl-3" key={card.label}>
              <article className="card metric-card h-100 border-0 shadow-sm rounded-4">
                <div className="card-body p-4">
                  <p className="text-uppercase small text-secondary fw-semibold mb-2">{card.label}</p>
                  <div className="d-flex align-items-end justify-content-between gap-3">
                    <h2 className="display-6 fw-bold mb-0">{card.value}</h2>
                    <span className={`badge rounded-pill text-bg-${card.tone === 'warning' ? 'warning' : 'success'} px-3 py-2`}>
                      {card.delta}
                    </span>
                  </div>
                </div>
              </article>
            </div>
          ))}
        </div>

        <div className="row g-4 mb-4">
          <div className="col-12 col-xl-8">
            <SpendingTrendChart data={spendingTrend} />
          </div>

          <div className="col-12 col-xl-4">
            <div className="d-grid gap-4 h-100">
              <AnalyticsInsights insights={aiInsights} />
              <section className="analytics-card rounded-4 p-4 p-lg-5 h-100">
                <p className="text-uppercase small text-secondary fw-semibold mb-1">AI Summary</p>
                <h3 className="h4 fw-bold mb-3">Live assistant output</h3>
                <p className="text-secondary mb-4">{aiSummary}</p>
                <div className="mb-4">
                  <p className="text-uppercase small text-secondary fw-semibold mb-2">Recommendations</p>
                  <div className="d-grid gap-2">
                    {aiRecommendations.length > 0 ? (
                      aiRecommendations.map((recommendation) => (
                        <div className="insight-card rounded-4 p-3" key={recommendation}>
                          <p className="mb-0 text-secondary">{recommendation}</p>
                        </div>
                      ))
                    ) : (
                      <div className="insight-card rounded-4 p-3">
                        <p className="mb-0 text-secondary">Recommendations will appear here once AI finishes analyzing.</p>
                      </div>
                    )}
                  </div>
                </div>
                <span className={`badge rounded-pill text-bg-${aiSource === 'gemini' ? 'success' : 'secondary'} px-3 py-2`}>
                  {aiSource === 'gemini' ? 'Gemini powered' : 'Fallback analysis'}
                </span>
              </section>
            </div>
          </div>
        </div>

        <div className="row g-4">
          <div className="col-12 col-xl-7">
            <section className="card border-0 shadow-sm rounded-4 h-100">
              <div className="card-body p-4 p-lg-5">
                <div className="d-flex justify-content-between align-items-center gap-3 mb-4">
                  <div>
                    <p className="text-uppercase small text-secondary fw-semibold mb-1">Recent Activity</p>
                    <h3 className="h4 fw-bold mb-0">Latest transactions</h3>
                  </div>
                  <button className="btn btn-sm btn-outline-primary" type="button">
                    View all
                  </button>
                </div>

                <div className="list-group list-group-flush">
                  {recentTransactions.map((transaction) => (
                    <div className="list-group-item px-0 py-3 border-0 transaction-row" key={`${transaction.title}-${transaction.date}`}>
                      <div className="d-flex justify-content-between align-items-center gap-3">
                        <div>
                          <h4 className="h6 fw-bold mb-1">{transaction.title}</h4>
                          <p className="mb-0 text-secondary">{transaction.category} · {transaction.date}</p>
                        </div>
                        <span className={`fw-semibold ${transaction.amount.startsWith('+') ? 'text-success' : 'text-danger'}`}>
                          {transaction.amount}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </section>
          </div>

          <div className="col-12 col-xl-5">
            <CategoryDistributionChart items={categoryBreakdown} />
          </div>
        </div>
      </section>
    </main>
  );
}
