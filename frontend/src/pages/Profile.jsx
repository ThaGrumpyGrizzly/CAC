import { useState, useEffect } from 'react'
import { useInvestments } from '../context/InvestmentContext'
import { User, Settings, Bell, Shield, Globe, DollarSign, TrendingUp, Save, Lock } from 'lucide-react'
import LoadingSpinner from '../components/LoadingSpinner'
import axios from 'axios'

const Profile = () => {
  const { user, loading, error } = useInvestments()
  const [isEditing, setIsEditing] = useState(false)
  const [saveLoading, setSaveLoading] = useState(false)
  const [userProfile, setUserProfile] = useState(null)
  const [showPasswordChange, setShowPasswordChange] = useState(false)
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  })
  const [passwordLoading, setPasswordLoading] = useState(false)
  const [passwordMessage, setPasswordMessage] = useState('')
  const [passwordError, setPasswordError] = useState('')
  const [preferences, setPreferences] = useState({
    // Personal Information
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    country: '',
    
    // Investment Preferences
    defaultCurrency: 'EUR',
    riskTolerance: 'moderate',
    investmentGoals: [],
    preferredAssetTypes: [],
    
    // Notification Settings
    emailNotifications: true,
    priceAlerts: true,
    portfolioUpdates: true,
    marketNews: false,
    
    // Privacy Settings
    profileVisibility: 'private',
    sharePortfolio: false,
    
    // Display Preferences
    theme: 'light',
    language: 'en',
    timezone: 'Europe/Amsterdam',
    
    // Trading Preferences
    autoRebalance: false,
    dividendReinvestment: true,
    taxLossHarvesting: false
  })

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

  const fetchUserProfile = async () => {
    try {
      const token = localStorage.getItem('token')
      if (!token) return

      const response = await axios.get(`${API_BASE_URL}/profile`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      
      console.log('Fetched user profile:', response.data)
      setUserProfile(response.data)
      
      // Pre-fill preferences with user data
      setPreferences(prev => ({
        ...prev,
        firstName: response.data.first_name || '',
        lastName: response.data.last_name || '',
        email: response.data.email || '',
        phone: response.data.phone || '',
        country: response.data.country || ''
      }))
    } catch (err) {
      console.error('Error fetching user profile:', err)
    }
  }

  useEffect(() => {
    // Fetch user profile data first
    fetchUserProfile()
    
    // Then load other preferences from localStorage
    const savedPreferences = localStorage.getItem('userPreferences')
    if (savedPreferences) {
      const parsed = JSON.parse(savedPreferences)
      setPreferences(prev => ({
        ...prev,
        ...parsed,
                 // Don't override profile data from API
         firstName: prev.firstName || parsed.firstName || '',
         lastName: prev.lastName || parsed.lastName || '',
         email: prev.email || parsed.email || '',
         phone: prev.phone || parsed.phone || '',
         country: prev.country || parsed.country || ''
      }))
    }
  }, [])

  const handlePreferenceChange = (key, value) => {
    setPreferences(prev => ({
      ...prev,
      [key]: value
    }))
  }

  const handleSave = async () => {
    setSaveLoading(true)
    try {
      const token = localStorage.getItem('token')
      if (!token) {
        throw new Error('No authentication token found')
      }

      console.log('Sending profile update:', {
        first_name: preferences.firstName,
        last_name: preferences.lastName,
        email: preferences.email,
        phone: preferences.phone,
        country: preferences.country
      })

      // Update user profile in database
      const response = await axios.put(`${API_BASE_URL}/profile`, {
        first_name: preferences.firstName,
        last_name: preferences.lastName,
        email: preferences.email,
        phone: preferences.phone,
        country: preferences.country
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })

      console.log('Profile update response:', response.data)

      // Update local user profile state
      setUserProfile(response.data)
      
      // Save other preferences to localStorage
      localStorage.setItem('userPreferences', JSON.stringify(preferences))
      setIsEditing(false)
      
      // Show success message
      alert('Profile updated successfully!')
    } catch (error) {
      console.error('Error saving profile:', error)
      console.error('Error details:', error.response?.data)
      alert(`Failed to save profile: ${error.response?.data?.detail || error.message}`)
    } finally {
      setSaveLoading(false)
    }
  }

  const handleCancel = () => {
    // Reset to saved preferences
    const savedPreferences = localStorage.getItem('userPreferences')
    if (savedPreferences) {
      setPreferences(JSON.parse(savedPreferences))
    }
    setIsEditing(false)
  }

  const handlePasswordChange = async (e) => {
    e.preventDefault()
    setPasswordLoading(true)
    setPasswordError('')
    setPasswordMessage('')

    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setPasswordError('New passwords do not match')
      setPasswordLoading(false)
      return
    }

    if (passwordData.newPassword.length < 6) {
      setPasswordError('New password must be at least 6 characters long')
      setPasswordLoading(false)
      return
    }

    try {
      const token = localStorage.getItem('token')
      const response = await axios.post(`${API_BASE_URL}/change-password`, {
        current_password: passwordData.currentPassword,
        new_password: passwordData.newPassword
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })

      if (response.data.success) {
        setPasswordMessage('Password changed successfully!')
        setPasswordData({
          currentPassword: '',
          newPassword: '',
          confirmPassword: ''
        })
        setShowPasswordChange(false)
      }
    } catch (error) {
      console.error('Error changing password:', error)
      setPasswordError(error.response?.data?.detail || 'Failed to change password. Please try again.')
    } finally {
      setPasswordLoading(false)
    }
  }

  if (loading) {
    return <LoadingSpinner />
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <div className="text-red-600 mb-4">{error}</div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Profile & Preferences</h1>
          <p className="text-gray-600 mt-1">Manage your personal information and investment preferences</p>
        </div>
        <div className="flex space-x-3">
          {isEditing ? (
            <>
              <button
                onClick={handleCancel}
                className="btn-secondary"
                disabled={saveLoading}
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                className="btn-primary flex items-center"
                disabled={saveLoading}
              >
                {saveLoading ? (
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                ) : (
                  <Save className="w-4 h-4 mr-2" />
                )}
                Save Changes
              </button>
            </>
          ) : (
            <button
              onClick={() => setIsEditing(true)}
              className="btn-primary flex items-center"
            >
              <Settings className="w-4 h-4 mr-2" />
              Edit Profile
            </button>
          )}
        </div>
      </div>

      {/* User Information Summary */}
      {userProfile && (
        <div className="card bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
          <div className="flex items-center mb-4">
            <User className="w-5 h-5 text-blue-600 mr-2" />
            <h2 className="text-xl font-semibold text-gray-900">Account Information</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <p className="text-gray-900 font-medium">{userProfile.email}</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
              <p className="text-gray-900 font-medium">{userProfile.username}</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Member Since</label>
              <p className="text-gray-900">{new Date(userProfile.created_at).toLocaleDateString()}</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Account Type</label>
              <p className="text-gray-900">{userProfile.is_admin ? 'Administrator' : 'Standard User'}</p>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Personal Information */}
        <div className="lg:col-span-2 space-y-6">
          {/* Personal Details */}
          <div className="card">
            <div className="flex items-center mb-4">
              <User className="w-5 h-5 text-primary-600 mr-2" />
              <h2 className="text-xl font-semibold text-gray-900">Personal Information</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  First Name
                </label>
                <input
                  type="text"
                  value={preferences.firstName}
                  onChange={(e) => handlePreferenceChange('firstName', e.target.value)}
                  disabled={!isEditing}
                  className="form-input"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Last Name
                </label>
                <input
                  type="text"
                  value={preferences.lastName}
                  onChange={(e) => handlePreferenceChange('lastName', e.target.value)}
                  disabled={!isEditing}
                  className="form-input"
                />
              </div>
                             <div>
                 <label className="block text-sm font-medium text-gray-700 mb-1">
                   Email
                 </label>
                 <input
                   type="email"
                   value={preferences.email || userProfile?.email || ''}
                   onChange={(e) => handlePreferenceChange('email', e.target.value)}
                   disabled={!isEditing}
                   className={!isEditing ? "form-input bg-gray-50" : "form-input"}
                 />
                 {isEditing && (
                   <p className="text-xs text-gray-500 mt-1">
                     Changing your email will affect your login credentials
                   </p>
                 )}
               </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Phone
                </label>
                <input
                  type="tel"
                  value={preferences.phone}
                  onChange={(e) => handlePreferenceChange('phone', e.target.value)}
                  disabled={!isEditing}
                  className="form-input"
                />
              </div>
            </div>
          </div>

          {/* Password Change */}
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <Lock className="w-5 h-5 text-primary-600 mr-2" />
                <h2 className="text-xl font-semibold text-gray-900">Password</h2>
              </div>
              {!showPasswordChange && (
                <button
                  onClick={() => setShowPasswordChange(true)}
                  className="text-sm text-indigo-600 hover:text-indigo-500"
                >
                  Change Password
                </button>
              )}
            </div>
            
            {showPasswordChange ? (
              <form onSubmit={handlePasswordChange} className="space-y-4">
                {passwordError && (
                  <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                    {passwordError}
                  </div>
                )}
                {passwordMessage && (
                  <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
                    {passwordMessage}
                  </div>
                )}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Current Password
                  </label>
                  <input
                    type="password"
                    required
                    value={passwordData.currentPassword}
                    onChange={(e) => setPasswordData(prev => ({ ...prev, currentPassword: e.target.value }))}
                    className="form-input"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    New Password
                  </label>
                  <input
                    type="password"
                    required
                    value={passwordData.newPassword}
                    onChange={(e) => setPasswordData(prev => ({ ...prev, newPassword: e.target.value }))}
                    className="form-input"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Confirm New Password
                  </label>
                  <input
                    type="password"
                    required
                    value={passwordData.confirmPassword}
                    onChange={(e) => setPasswordData(prev => ({ ...prev, confirmPassword: e.target.value }))}
                    className="form-input"
                  />
                </div>
                <div className="flex space-x-3">
                  <button
                    type="submit"
                    disabled={passwordLoading}
                    className="btn-primary flex items-center"
                  >
                    {passwordLoading ? (
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    ) : (
                      <Save className="w-4 h-4 mr-2" />
                    )}
                    {passwordLoading ? 'Changing...' : 'Change Password'}
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setShowPasswordChange(false)
                      setPasswordData({
                        currentPassword: '',
                        newPassword: '',
                        confirmPassword: ''
                      })
                      setPasswordError('')
                      setPasswordMessage('')
                    }}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            ) : (
              <p className="text-gray-600 text-sm">
                Keep your account secure by using a strong password that you don't use elsewhere.
              </p>
            )}
          </div>

          {/* Investment Preferences */}
          <div className="card">
            <div className="flex items-center mb-4">
              <TrendingUp className="w-5 h-5 text-primary-600 mr-2" />
              <h2 className="text-xl font-semibold text-gray-900">Investment Preferences</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Default Currency
                </label>
                <select
                  value={preferences.defaultCurrency}
                  onChange={(e) => handlePreferenceChange('defaultCurrency', e.target.value)}
                  disabled={!isEditing}
                  className="form-select"
                >
                  <option value="EUR">EUR (Euro)</option>
                  <option value="USD">USD (US Dollar)</option>
                  <option value="GBP">GBP (British Pound)</option>
                  <option value="CHF">CHF (Swiss Franc)</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Risk Tolerance
                </label>
                <select
                  value={preferences.riskTolerance}
                  onChange={(e) => handlePreferenceChange('riskTolerance', e.target.value)}
                  disabled={!isEditing}
                  className="form-select"
                >
                  <option value="conservative">Conservative</option>
                  <option value="moderate">Moderate</option>
                  <option value="aggressive">Aggressive</option>
                </select>
              </div>
            </div>
          </div>

          {/* Trading Preferences */}
          <div className="card">
            <div className="flex items-center mb-4">
              <DollarSign className="w-5 h-5 text-primary-600 mr-2" />
              <h2 className="text-xl font-semibold text-gray-900">Trading Preferences</h2>
            </div>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700">Auto Rebalancing</label>
                  <p className="text-xs text-gray-500">Automatically rebalance portfolio based on target allocation</p>
                </div>
                <input
                  type="checkbox"
                  checked={preferences.autoRebalance}
                  onChange={(e) => handlePreferenceChange('autoRebalance', e.target.checked)}
                  disabled={!isEditing}
                  className="form-checkbox"
                />
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700">Dividend Reinvestment</label>
                  <p className="text-xs text-gray-500">Automatically reinvest dividends</p>
                </div>
                <input
                  type="checkbox"
                  checked={preferences.dividendReinvestment}
                  onChange={(e) => handlePreferenceChange('dividendReinvestment', e.target.checked)}
                  disabled={!isEditing}
                  className="form-checkbox"
                />
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700">Tax Loss Harvesting</label>
                  <p className="text-xs text-gray-500">Automatically harvest tax losses</p>
                </div>
                <input
                  type="checkbox"
                  checked={preferences.taxLossHarvesting}
                  onChange={(e) => handlePreferenceChange('taxLossHarvesting', e.target.checked)}
                  disabled={!isEditing}
                  className="form-checkbox"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Notification Settings */}
          <div className="card">
            <div className="flex items-center mb-4">
              <Bell className="w-5 h-5 text-primary-600 mr-2" />
              <h2 className="text-xl font-semibold text-gray-900">Notifications</h2>
            </div>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-gray-700">Email Notifications</label>
                <input
                  type="checkbox"
                  checked={preferences.emailNotifications}
                  onChange={(e) => handlePreferenceChange('emailNotifications', e.target.checked)}
                  disabled={!isEditing}
                  className="form-checkbox"
                />
              </div>
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-gray-700">Price Alerts</label>
                <input
                  type="checkbox"
                  checked={preferences.priceAlerts}
                  onChange={(e) => handlePreferenceChange('priceAlerts', e.target.checked)}
                  disabled={!isEditing}
                  className="form-checkbox"
                />
              </div>
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-gray-700">Portfolio Updates</label>
                <input
                  type="checkbox"
                  checked={preferences.portfolioUpdates}
                  onChange={(e) => handlePreferenceChange('portfolioUpdates', e.target.checked)}
                  disabled={!isEditing}
                  className="form-checkbox"
                />
              </div>
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-gray-700">Market News</label>
                <input
                  type="checkbox"
                  checked={preferences.marketNews}
                  onChange={(e) => handlePreferenceChange('marketNews', e.target.checked)}
                  disabled={!isEditing}
                  className="form-checkbox"
                />
              </div>
            </div>
          </div>

          {/* Privacy Settings */}
          <div className="card">
            <div className="flex items-center mb-4">
              <Shield className="w-5 h-5 text-primary-600 mr-2" />
              <h2 className="text-xl font-semibold text-gray-900">Privacy</h2>
            </div>
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Profile Visibility
                </label>
                <select
                  value={preferences.profileVisibility}
                  onChange={(e) => handlePreferenceChange('profileVisibility', e.target.value)}
                  disabled={!isEditing}
                  className="form-select"
                >
                  <option value="private">Private</option>
                  <option value="friends">Friends Only</option>
                  <option value="public">Public</option>
                </select>
              </div>
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-gray-700">Share Portfolio</label>
                <input
                  type="checkbox"
                  checked={preferences.sharePortfolio}
                  onChange={(e) => handlePreferenceChange('sharePortfolio', e.target.checked)}
                  disabled={!isEditing}
                  className="form-checkbox"
                />
              </div>
            </div>
          </div>

          {/* Display Preferences */}
          <div className="card">
            <div className="flex items-center mb-4">
              <Globe className="w-5 h-5 text-primary-600 mr-2" />
              <h2 className="text-xl font-semibold text-gray-900">Display</h2>
            </div>
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Theme
                </label>
                <select
                  value={preferences.theme}
                  onChange={(e) => handlePreferenceChange('theme', e.target.value)}
                  disabled={!isEditing}
                  className="form-select"
                >
                  <option value="light">Light</option>
                  <option value="dark">Dark</option>
                  <option value="auto">Auto</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Language
                </label>
                <select
                  value={preferences.language}
                  onChange={(e) => handlePreferenceChange('language', e.target.value)}
                  disabled={!isEditing}
                  className="form-select"
                >
                  <option value="en">English</option>
                  <option value="nl">Nederlands</option>
                  <option value="de">Deutsch</option>
                  <option value="fr">Français</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Timezone
                </label>
                <select
                  value={preferences.timezone}
                  onChange={(e) => handlePreferenceChange('timezone', e.target.value)}
                  disabled={!isEditing}
                  className="form-select"
                >
                  <option value="Europe/Amsterdam">Europe/Amsterdam</option>
                  <option value="Europe/London">Europe/London</option>
                  <option value="America/New_York">America/New_York</option>
                  <option value="Asia/Tokyo">Asia/Tokyo</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Profile 