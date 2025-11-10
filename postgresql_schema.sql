-- ==========================================
-- Database: SSIS_Webapp
-- ==========================================

-- Colleges Table
CREATE TABLE public.colleges (
    code VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Programs Table
CREATE TABLE public.programs (
    code VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    college_code VARCHAR(20),
    CONSTRAINT program_college_code_fkey
        FOREIGN KEY (college_code)
        REFERENCES public.colleges (code)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

-- Students Table
CREATE TABLE public.students (
    id VARCHAR(20) PRIMARY KEY,
    f_name VARCHAR(255) NOT NULL,
    l_name VARCHAR(255) NOT NULL,
    program VARCHAR(20),
    year_level VARCHAR(10) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    CONSTRAINT student_program_code_fkey
        FOREIGN KEY (program)
        REFERENCES public.programs (code)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

-- Users Table
CREATE TABLE public.users (
    id BIGINT GENERATED ALWAYS AS IDENTITY
        (START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1),
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    password_length INTEGER,
    CONSTRAINT users_pkey PRIMARY KEY (id)
);

-- Activity Logs Table
CREATE TABLE public.activity_logs (
    id INTEGER GENERATED ALWAYS AS IDENTITY
        (START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1),
    message TEXT NOT NULL,
    icon VARCHAR(50),
    "timestamp" TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT activity_logs_pkey PRIMARY KEY (id)
);

-- ==========================================
-- OWNERSHIP (if using postgres as default user)
-- ==========================================
ALTER TABLE public.colleges OWNER TO postgres;
ALTER TABLE public.programs OWNER TO postgres;
ALTER TABLE public.students OWNER TO postgres;
ALTER TABLE public.users OWNER TO postgres;
ALTER TABLE public.activity_logs OWNER TO postgres;

-- ==========================================
-- END OF SCHEMA
-- ==========================================
