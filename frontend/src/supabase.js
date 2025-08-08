import { createClient } from '@supabase/supabase-js'

// Your Supabase config - replace with your actual config from Supabase Dashboard
const supabaseUrl = 'https://your-project.supabase.co'
const supabaseAnonKey = 'your-anon-key-here'

export const supabase = createClient(supabaseUrl, supabaseAnonKey) 