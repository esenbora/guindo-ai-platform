# Supabase Database Setup

Run these SQL commands in your Supabase SQL Editor (Dashboard > SQL Editor > New Query)

## 1. Create Users Table

```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  whop_user_id TEXT UNIQUE NOT NULL,
  email TEXT,
  name TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Users can only read their own data
CREATE POLICY "Users can read own data"
  ON users
  FOR SELECT
  USING (auth.uid()::text = whop_user_id);

-- Create index on whop_user_id for faster lookups
CREATE INDEX idx_users_whop_id ON users(whop_user_id);
```

## 2. Create Analyses Table

```sql
-- Analyses table
CREATE TABLE analyses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,

  -- Store user profile data
  profile_data JSONB NOT NULL,

  -- Store analysis results
  career_analysis TEXT NOT NULL,
  roi_analysis TEXT NOT NULL,
  fire_analysis TEXT NOT NULL,
  side_hustle_analysis TEXT NOT NULL,
  interests_roadmap TEXT NOT NULL,

  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE analyses ENABLE ROW LEVEL SECURITY;

-- Users can only read their own analyses
CREATE POLICY "Users can read own analyses"
  ON analyses
  FOR SELECT
  USING (user_id IN (
    SELECT id FROM users WHERE whop_user_id = auth.uid()::text
  ));

-- Create index on user_id for faster lookups
CREATE INDEX idx_analyses_user_id ON analyses(user_id);
CREATE INDEX idx_analyses_created_at ON analyses(created_at DESC);
```

## 3. Create Payments Table

```sql
-- Payments table
CREATE TABLE payments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  whop_payment_id TEXT UNIQUE NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('pending', 'completed', 'failed')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;

-- Users can only read their own payments
CREATE POLICY "Users can read own payments"
  ON payments
  FOR SELECT
  USING (user_id IN (
    SELECT id FROM users WHERE whop_user_id = auth.uid()::text
  ));

-- Create index on whop_payment_id for faster lookups
CREATE INDEX idx_payments_whop_id ON payments(whop_payment_id);
CREATE INDEX idx_payments_user_id ON payments(user_id);
```

## 4. Create Updated_At Trigger

```sql
-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for users table
CREATE TRIGGER update_users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

## 5. Verify Setup

```sql
-- Check if all tables exist
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN ('users', 'analyses', 'payments');

-- Should return 3 rows
```

## Next Steps

1. ✅ Run all SQL commands above in Supabase SQL Editor
2. ✅ Verify tables are created (check Tables section in dashboard)
3. ✅ Get your API credentials from Settings > API
4. ✅ Add credentials to `.env.local` file
5. ✅ Test the connection from your app

## Optional: Insert Test Data

```sql
-- Insert a test user (for development only)
INSERT INTO users (whop_user_id, email, name)
VALUES ('test_user_123', 'test@example.com', 'Test User');

-- Verify
SELECT * FROM users;
```

## Row Level Security (RLS) Notes

- RLS is enabled on all tables
- Users can only access their own data
- This ensures data privacy and security
- Policies are automatically enforced by Supabase

## Important Security Notes

⚠️ **NEVER** commit your actual `.env.local` file to git!
✅ Only commit `.env.local.example` with placeholder values
🔐 Keep your Supabase keys secure
🔑 Use environment variables for all sensitive data
