import { useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'

const ForgotPassword = () => {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [showResetForm, setShowResetForm] = useState(false)
  const [resetToken, setResetToken] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

  const handleRequestReset = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setMessage('')

    try {
      const response = await axios.post(`${API_BASE_URL}/forgot-password`, {
        email: email
      })

      if (response.data.success) {
        setMessage(response.data.message)
        // For development, show the token in console
        console.log('Check the backend console for the reset token')
      }
    } catch (error) {
      console.error('Error requesting password reset:', error)
      setError('Failed to send reset email. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleResetPassword = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match')
      setLoading(false)
      return
    }

    if (newPassword.length < 6) {
      setError('Password must be at least 6 characters long')
      setLoading(false)
      return
    }

    try {
      const response = await axios.post(`${API_BASE_URL}/reset-password`, {
        email: email,
        reset_token: resetToken,
        new_password: newPassword
      })

      if (response.data.success) {
        setMessage('Password reset successful! You can now login with your new password.')
        setShowResetForm(false)
        setResetToken('')
        setNewPassword('')
        setConfirmPassword('')
      }
    } catch (error) {
      console.error('Error resetting password:', error)
      setError(error.response?.data?.detail || 'Failed to reset password. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className='min-h-screen flex items-center justify-center bg-gray-50'>
      <div className='max-w-md w-full space-y-8'>
        <div>
          <h2 className='mt-6 text-center text-3xl font-extrabold text-gray-900'>
            Reset your password
          </h2>
          <p className='mt-2 text-center text-sm text-gray-600'>
            Or{' '}
            <Link to='/login' className='font-medium text-indigo-600 hover:text-indigo-500'>
              sign in to your account
            </Link>
          </p>
        </div>

        {!showResetForm ? (
          // Request reset form
          <form className='mt-8 space-y-6' onSubmit={handleRequestReset}>
            {error && (
              <div className='bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded'>
                {error}
              </div>
            )}
            {message && (
              <div className='bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded'>
                {message}
              </div>
            )}
            <div>
              <input
                type='email'
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder='Email address'
                className='appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm'
              />
            </div>
            <div>
              <button
                type='submit'
                disabled={loading}
                className='group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50'
              >
                {loading ? 'Sending...' : 'Send reset link'}
              </button>
            </div>
            {message && (
              <div className='text-center'>
                <button
                  type='button'
                  onClick={() => setShowResetForm(true)}
                  className='text-sm text-indigo-600 hover:text-indigo-500'
                >
                  I have my reset token
                </button>
              </div>
            )}
          </form>
        ) : (
          // Reset password form
          <form className='mt-8 space-y-6' onSubmit={handleResetPassword}>
            {error && (
              <div className='bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded'>
                {error}
              </div>
            )}
            {message && (
              <div className='bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded'>
                {message}
              </div>
            )}
            <div>
              <input
                type='text'
                required
                value={resetToken}
                onChange={(e) => setResetToken(e.target.value)}
                placeholder='Reset token'
                className='appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm'
              />
            </div>
            <div>
              <input
                type='password'
                required
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder='New password'
                className='appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm'
              />
            </div>
            <div>
              <input
                type='password'
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder='Confirm new password'
                className='appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm'
              />
            </div>
            <div>
              <button
                type='submit'
                disabled={loading}
                className='group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50'
              >
                {loading ? 'Resetting...' : 'Reset password'}
              </button>
            </div>
            <div className='text-center'>
              <button
                type='button'
                onClick={() => setShowResetForm(false)}
                className='text-sm text-gray-600 hover:text-gray-500'
              >
                Back to request form
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  )
}

export default ForgotPassword 