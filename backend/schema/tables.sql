CREATE TABLE "user"(
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    username text UNIQUE NOT NULL,
    email text UNIQUE,
    hashed_password text NOT NULL,
    "disabled" boolean NOT NULL DEFAULT FALSE
);

CREATE TABLE category(
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text UNIQUE NOT NULL
);

CREATE TABLE merchant(
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text UNIQUE NOT NULL
);

CREATE TABLE "transaction"(
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    amount decimal NOT NULL,
    "date" date NOT NULL,
    user_id uuid NOT NULL REFERENCES "user",
    merchant_id uuid NOT NULL REFERENCES merchant,
    category_id uuid NOT NULL REFERENCES category
);

CREATE INDEX transaction_user_date_idx ON "transaction"(user_id, "date", id DESC);

CREATE TABLE budget(
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    amount decimal NOT NULL,
    category_id uuid NOT NULL REFERENCES category,
    user_id uuid NOT NULL REFERENCES "user",
    UNIQUE (category_id, user_id)
);

