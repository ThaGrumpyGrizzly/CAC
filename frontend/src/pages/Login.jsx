import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import axios from 'axios'

const Login = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const API_BASE_URL = 'https://cac-production.up.railway.app'
      console.log('Using API URL:', API_BASE_URL)
      console.log('Sending login data:', JSON.stringify({ email, password }))
      console.log('Making request to:', `${API_BASE_URL}/login`)
      const response = await axios.post(`${API_BASE_URL}/login`, {
        email,
        password
      })

      // Store token
      localStorage.setItem('token', response.data.access_token)
      
      // Redirect to dashboard
      navigate('/dashboard')
    } catch (error) {
      console.log('Login error:', JSON.stringify(error.response?.data || error.message))
      setError('Invalid email or password')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className='min-h-screen flex items-center justify-center bg-gray-50'>
      <div className='max-w-md w-full space-y-8'>
        <div>
          <h2 className='mt-6 text-center text-3xl font-extrabold text-gray-900'>
            Sign in to your account
          </h2>
          <p className='mt-2 text-center text-sm text-gray-600'>
            Or{' '}
            <Link to='/register' className='font-medium text-indigo-600 hover:text-indigo-500'>
              create a new account
            </Link>
          </p>
        </div>
        <form className='mt-8 space-y-6' onSubmit={handleSubmit}>
          {error && (
            <div className='bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded'>
              {error}
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
            <input
              type='password'
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder='Password'
              className='appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm'
            />
          </div>
          <div>
            <button
              type='submit'
              disabled={loading}
              className='group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50'
            >
              {loading ? 'Signing in...' : 'Sign in'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default Login
