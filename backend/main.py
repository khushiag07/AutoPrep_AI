from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.pipeline.profiler import DataProfiler
from app.pipeline.intelligence import DataIntelligence
from app.pipeline.validator import DataValidator
from app.pipeline.cleaner import CleaningEngine
import pandas as pd
import io


app = FastAPI(
    title="AutoPrep AI",
    description="Intelligent Data Preparation Pipeline",
    version="1.0.0"
)


# ==============================
# CORS
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
# HEALTH CHECK
# ==============================

@app.get("/")
def root():
    return {
        "message": "AutoPrep AI backend is running"
    }


# ==============================
# DATASET UPLOAD
# ==============================

@app.post("/upload")

async def upload_dataset(
    file: UploadFile = File(...)
    
):

    contents = await file.read()

    filename = file.filename.lower()

    try:

        # --------------------------
        # READ CSV
        # --------------------------

        if filename.endswith(".csv"):

            df = pd.read_csv(
                io.BytesIO(contents)
            )

        # --------------------------
        # READ EXCEL
        # --------------------------

        elif filename.endswith(
            (".xlsx", ".xls")
        ):

            df = pd.read_excel(
                io.BytesIO(contents)
            )

        else:

            return {
                "success": False,
                "error": "Only CSV and Excel files are supported."
            }
        profiler = DataProfiler(df)

        profile = profiler.profile()

        intelligence = DataIntelligence()

        analysis = intelligence.analyze(
    profile,
    df
)
        cleaner = CleaningEngine(
            df,
            analysis["recommendations"]
        )

        cleaned_df, audit_log = cleaner.clean()
        validator = DataValidator(
    df,
    cleaned_df
)

        validation = validator.validate()
                

    


        # ==========================
        # BASIC PROFILING
        # ==========================

        rows = len(df)

        columns = len(df.columns)

        missing_values = int(
            df.isnull().sum().sum()
        )

        duplicate_rows = int(
            df.duplicated().sum()
        )


        # Column information

        column_details = []

        for column in df.columns:

            missing = int(
                df[column].isnull().sum()
            )

            unique = int(
                df[column].nunique()
            )

            dtype = str(
                df[column].dtype
            )

            column_details.append({
                "name": column,
                "dtype": dtype,
                "missing": missing,
                "unique": unique
            })


        # ==========================
        # RESPONSE
        # ==========================
        return {
        "success": True,

        "filename": file.filename,

        "profile": profile,

        "intelligence": analysis,

        "cleaning": {
            "audit_log": audit_log,

            "original_rows": len(df),

            "cleaned_rows": len(cleaned_df),

            "original_columns": len(df.columns),

            "cleaned_columns": len(cleaned_df.columns)
        },

    "validation": validation
}




    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }