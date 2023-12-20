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
    merchant_id uuid NOT NULL REFERENCES merchant,
    category_id uuid NOT NULL REFERENCES category
);


CREATE TABLE budget(
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    amount decimal NOT NULL,
    category_id uuid NOT NULL UNIQUE REFERENCES category
);
