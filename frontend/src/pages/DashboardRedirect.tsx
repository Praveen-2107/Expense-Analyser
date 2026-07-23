import { useAuth } from '../context/AuthContext';

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

  const aiInsights = [
    'Dining expenses are 18% higher than last month. Set a weekly cap to stay within plan.',
    'You have $1,140 remaining in your monthly budget with 9 days left to reset.',
    'Recurring subscriptions are stable, but one unused service could save $12/month.'
  ] as const;

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
            <section className="card border-0 shadow-sm rounded-4 h-100">
              <div className="card-body p-4 p-lg-5">
                <div className="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-4">
                  <div>
                    <p className="text-uppercase small text-secondary fw-semibold mb-1">Spending Trend</p>
                    <h3 className="h4 fw-bold mb-0">Last 6 months overview</h3>
                  </div>
                  <span className="badge rounded-pill text-bg-light border text-secondary px-3 py-2">Chart preview</span>
                </div>

                <div className="trend-chart d-flex align-items-end gap-3 mb-4">
                  {[58, 46, 72, 64, 88, 76].map((height, index) => (
                    <div className="trend-column" key={index}>
                      <div className="trend-bar" style={{ height: `${height}%` }} />
                      <span className="trend-label">M{index + 1}</span>
                    </div>
                  ))}
                </div>

                <div className="row g-3">
                  <div className="col-md-4">
                    <div className="info-tile rounded-4 p-3 h-100">
                      <p className="text-secondary small mb-1">Highest spend category</p>
                      <h4 className="h5 fw-bold mb-1">Housing</h4>
                      <p className="mb-0 text-secondary">34% of monthly spending</p>
                    </div>
                  </div>
                  <div className="col-md-4">
                    <div className="info-tile rounded-4 p-3 h-100">
                      <p className="text-secondary small mb-1">Projected savings</p>
                      <h4 className="h5 fw-bold mb-1">$1,320</h4>
                      <p className="mb-0 text-secondary">If current pace continues</p>
                    </div>
                  </div>
                  <div className="col-md-4">
                    <div className="info-tile rounded-4 p-3 h-100">
                      <p className="text-secondary small mb-1">Budget alerts</p>
                      <h4 className="h5 fw-bold mb-1">2 active</h4>
                      <p className="mb-0 text-secondary">Subscriptions and dining</p>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>

          <div className="col-12 col-xl-4">
            <section className="card border-0 shadow-sm rounded-4 h-100">
              <div className="card-body p-4 p-lg-5">
                <p className="text-uppercase small text-secondary fw-semibold mb-1">AI Insights</p>
                <h3 className="h4 fw-bold mb-4">What the assistant sees</h3>
                <div className="d-grid gap-3">
                  {aiInsights.map((insight) => (
                    <div className="insight-card rounded-4 p-3" key={insight}>
                      <p className="mb-0 text-secondary">{insight}</p>
                    </div>
                  ))}
                </div>
              </div>
            </section>
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
            <section className="card border-0 shadow-sm rounded-4 h-100">
              <div className="card-body p-4 p-lg-5">
                <p className="text-uppercase small text-secondary fw-semibold mb-1">Budget Planner</p>
                <h3 className="h4 fw-bold mb-4">Category allocation</h3>

                <div className="d-grid gap-3">
                  {categoryBreakdown.map((item) => (
                    <div key={item.name}>
                      <div className="d-flex justify-content-between align-items-center mb-2">
                        <span className="fw-semibold">{item.name}</span>
                        <span className="text-secondary">{item.amount}</span>
                      </div>
                      <div className="progress budget-progress">
                        <div className={`progress-bar ${item.color}`} style={{ width: `${item.percent}%` }} />
                      </div>
                    </div>
                  ))}
                </div>

                <div className="mt-4 p-3 rounded-4 budget-summary">
                  <p className="text-uppercase small text-secondary fw-semibold mb-1">Next recommendation</p>
                  <h4 className="h5 fw-bold mb-2">Reduce dining by 10%</h4>
                  <p className="mb-0 text-secondary">
                    That would improve your monthly savings by roughly $112 without affecting recurring essentials.
                  </p>
                </div>
              </div>
            </section>
          </div>
        </div>
      </section>
    </main>
  );
}
