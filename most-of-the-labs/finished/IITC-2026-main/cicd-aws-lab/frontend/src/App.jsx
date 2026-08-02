import { useState, useEffect } from 'react'

const API_URL = import.meta.env.VITE_API_URL || (
  window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : `http://${window.location.hostname}:8000`
)

function App() {
  const [stats, setStats] = useState(null)
  const [restaurants, setRestaurants] = useState([])
  const [menuItems, setMenuItems] = useState([])
  const [selectedRestaurant, setSelectedRestaurant] = useState(null)
  const [activeTab, setActiveTab] = useState('dashboard')
  const [backendStatus, setBackendStatus] = useState('checking') // 'connected' | 'disconnected' | 'checking'

  useEffect(() => {
    const checkBackend = () => {
      fetch(`${API_URL}/`)
        .then(r => {
          if (r.ok) setBackendStatus('connected')
          else setBackendStatus('disconnected')
        })
        .catch(() => setBackendStatus('disconnected'))
    }

    checkBackend()
    const interval = setInterval(checkBackend, 5000)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    fetch(`${API_URL}/api/stats`).then(r => r.json()).then(setStats).catch(() => {})
    fetch(`${API_URL}/api/restaurants`).then(r => r.json()).then(setRestaurants).catch(() => {})
    fetch(`${API_URL}/api/menu-items`).then(r => r.json()).then(setMenuItems).catch(() => {})
  }, [])

  const filteredItems = selectedRestaurant
    ? menuItems.filter(i => i.restaurant === selectedRestaurant)
    : menuItems

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <header className="border-b border-indigo-500/20 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center text-white font-bold text-lg">
              D
            </div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-indigo-200 to-purple-200 bg-clip-text text-transparent">
              DataBite
            </h1>
          </div>
          <div className="flex items-center gap-4">
            <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium border ${
              backendStatus === 'connected'
                ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
                : backendStatus === 'disconnected'
                ? 'bg-red-500/10 border-red-500/30 text-red-400'
                : 'bg-yellow-500/10 border-yellow-500/30 text-yellow-400'
            }`}>
              <span className={`w-2 h-2 rounded-full ${
                backendStatus === 'connected' ? 'bg-emerald-400 animate-pulse' :
                backendStatus === 'disconnected' ? 'bg-red-400' : 'bg-yellow-400 animate-pulse'
              }`}></span>
              {backendStatus === 'connected' ? 'API Connected' :
               backendStatus === 'disconnected' ? 'API Disconnected' : 'Checking...'}
            </div>
          </div>
          <nav className="flex gap-1">
            {['dashboard', 'restaurants', 'menu'].map(tab => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-4 py-2 rounded-lg text-sm font-medium capitalize transition-all ${
                  activeTab === tab
                    ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700/50'
                }`}
              >
                {tab}
              </button>
            ))}
          </nav>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-10">
        {/* Dashboard */}
        {activeTab === 'dashboard' && (
          <div>
            <div className="mb-10">
              <h1 className="text-2xl font-bold text-emerald-400 mb-4">CI/CD Pipeline Deployment Successful</h1>
              <h2 className="text-3xl font-bold text-white mb-2">Dashboard</h2>
              <p className="text-slate-400">Real-time restaurant menu data collection overview</p>
            </div>

            {/* Stats Cards */}
            {stats && (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-10">
                <StatCard label="Restaurants" value={stats.total_restaurants} icon="🏪" color="indigo" />
                <StatCard label="Menu Items" value={stats.total_menu_items} icon="🍽️" color="emerald" />
                <StatCard label="Cuisines" value={stats.cuisines_tracked} icon="🌍" color="amber" />
                <StatCard label="Cities" value={stats.cities_covered} icon="📍" color="rose" />
              </div>
            )}

            {/* About */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-slate-800/50 border border-slate-700/50 rounded-2xl p-7">
                <h3 className="text-lg font-semibold text-white mb-3">What is DataBite?</h3>
                <p className="text-slate-400 leading-relaxed">
                  DataBite collects and analyzes menu data from restaurants across Israel.
                  We track prices, categories, and trends to provide insights for the food industry.
                </p>
                <div className="mt-5 flex flex-wrap gap-2">
                  {['Menu Scraping', 'Price Tracking', 'Trend Analysis', 'API Access'].map(tag => (
                    <span key={tag} className="px-3 py-1 bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 rounded-full text-xs font-medium">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
              <div className="bg-slate-800/50 border border-slate-700/50 rounded-2xl p-7">
                <h3 className="text-lg font-semibold text-white mb-3">How It Works</h3>
                <div className="space-y-4">
                  {[
                    { step: '1', text: 'Restaurants are added to our system' },
                    { step: '2', text: 'We collect menu data periodically' },
                    { step: '3', text: 'Data is normalized and categorized' },
                    { step: '4', text: 'Insights are available via API & dashboard' },
                  ].map(item => (
                    <div key={item.step} className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center text-indigo-300 text-sm font-bold">
                        {item.step}
                      </div>
                      <span className="text-slate-300 text-sm">{item.text}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Restaurants */}
        {activeTab === 'restaurants' && (
          <div>
            <div className="mb-10">
              <h2 className="text-3xl font-bold text-white mb-2">Restaurants</h2>
              <p className="text-slate-400">All tracked restaurants in our database</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {restaurants.map(r => (
                <div
                  key={r.id}
                  onClick={() => { setSelectedRestaurant(r.name); setActiveTab('menu') }}
                  className="bg-slate-800/50 border border-slate-700/50 rounded-2xl p-6 hover:border-indigo-500/40 hover:-translate-y-1 transition-all cursor-pointer"
                >
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-white">{r.name}</h3>
                    <span className="text-yellow-400 text-sm font-medium">★ {r.rating}</span>
                  </div>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-400">Cuisine</span>
                      <span className="text-slate-200">{r.cuisine}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Location</span>
                      <span className="text-slate-200">{r.location}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Menu Items</span>
                      <span className="text-indigo-300 font-medium">{r.menu_items}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Menu Items */}
        {activeTab === 'menu' && (
          <div>
            <div className="mb-6 flex items-center justify-between flex-wrap gap-4">
              <div>
                <h2 className="text-3xl font-bold text-white mb-2">Menu Items</h2>
                <p className="text-slate-400">
                  {selectedRestaurant ? `Showing items from ${selectedRestaurant}` : 'All collected menu items'}
                </p>
              </div>
              {selectedRestaurant && (
                <button
                  onClick={() => setSelectedRestaurant(null)}
                  className="px-4 py-2 bg-slate-700/50 hover:bg-slate-600/50 border border-slate-600 text-slate-300 rounded-lg text-sm transition-all"
                >
                  Show All
                </button>
              )}
            </div>

            {/* Filter chips */}
            <div className="flex gap-2 mb-6 flex-wrap">
              <button
                onClick={() => setSelectedRestaurant(null)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  !selectedRestaurant ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30' : 'bg-slate-700/30 text-slate-400 border border-slate-600/50 hover:text-slate-200'
                }`}
              >
                All
              </button>
              {restaurants.map(r => (
                <button
                  key={r.id}
                  onClick={() => setSelectedRestaurant(r.name)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                    selectedRestaurant === r.name ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30' : 'bg-slate-700/30 text-slate-400 border border-slate-600/50 hover:text-slate-200'
                  }`}
                >
                  {r.name}
                </button>
              ))}
            </div>

            {/* Table */}
            <div className="bg-slate-800/50 border border-slate-700/50 rounded-2xl overflow-hidden">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-slate-700/50">
                    <th className="text-left px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">Item</th>
                    <th className="text-left px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">Restaurant</th>
                    <th className="text-left px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">Category</th>
                    <th className="text-right px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">Price</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredItems.map(item => (
                    <tr key={item.id} className="border-b border-slate-700/30 hover:bg-slate-700/20 transition-colors">
                      <td className="px-6 py-4 text-sm text-white font-medium">{item.name}</td>
                      <td className="px-6 py-4 text-sm text-slate-300">{item.restaurant}</td>
                      <td className="px-6 py-4">
                        <span className="px-2.5 py-1 bg-slate-700/50 text-slate-300 rounded-md text-xs">
                          {item.category}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-emerald-400 font-medium text-right">₪{item.price}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-700/30 mt-20">
        <div className="max-w-7xl mx-auto px-6 py-8 text-center text-slate-500 text-sm">
          DataBite © 2025 — Restaurant Menu Intelligence Platform
        </div>
      </footer>
    </div>
  )
}

function StatCard({ label, value, icon, color }) {
  const colors = {
    indigo: 'from-indigo-500/10 to-indigo-500/5 border-indigo-500/20',
    emerald: 'from-emerald-500/10 to-emerald-500/5 border-emerald-500/20',
    amber: 'from-amber-500/10 to-amber-500/5 border-amber-500/20',
    rose: 'from-rose-500/10 to-rose-500/5 border-rose-500/20',
  }

  return (
    <div className={`bg-gradient-to-br ${colors[color]} border rounded-2xl p-6`}>
      <div className="text-2xl mb-2">{icon}</div>
      <div className="text-3xl font-bold text-white">{value}</div>
      <div className="text-sm text-slate-400 mt-1">{label}</div>
    </div>
  )
}

export default App
