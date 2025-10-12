-- 原有的 names 表，予以保留
CREATE TABLE IF NOT EXISTS names (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL CHECK (char_length(name) <= 50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 新增 menu_items 表，用於存放菜單項目
CREATE TABLE IF NOT EXISTS menu_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    price NUMERIC(10, 2) NOT NULL
);

-- 新增 orders 表，用於存放訂單資訊
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    items JSONB NOT NULL, -- 用 JSONB 格式儲存訂單內容, e.g., '''[{"id": 1, "name": "Burger", "price": 150, "quantity": 1}]'''
    total_price NUMERIC(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending', -- e.g., 'pending', 'in_progress', 'completed'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 插入一些範例菜單項目，方便測試
INSERT INTO menu_items (name, price) VALUES
('經典漢堡', 150.00),
('起司漢堡', 170.00),
('培根漢堡', 180.00),
('薯條', 60.00),
('可樂', 40.00)
ON CONFLICT (name) DO NOTHING; -- 如果名稱已存在則不插入，避免重複