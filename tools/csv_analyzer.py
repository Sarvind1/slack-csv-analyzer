"""
CSV analysis tool with pandas code generation
"""

import os
import sys
import io
import logging
import traceback
from pathlib import Path
from typing import List
import tools.vectorstore as vs

import pandas as pd
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)


def analyze_csv_data(query: str) -> str:
    """Analyze CSV data using AI-generated pandas code."""
    try:
        logger.info(f"📊 Analyzing CSV data for: {query}")
        vectorstore = vs.get_vectorstore()
        docs = vectorstore.similarity_search(query, k=5,
                                     filter={"knowledge_path": "csv_descriptions"}
                                     )

        # Group documents by filename to avoid confusion between CSV files
        from collections import defaultdict
        files_content = defaultdict(list)
        identified_filenames = set()

        for doc in docs:
            filename = doc.metadata.get('filename', 'Unknown').replace('.md', '.csv')
            files_content[filename].append(doc.page_content)
            identified_filenames.add(doc.metadata.get('filename', 'Unknown'))

        logger.info(f"📂 Found {len(files_content)} unique CSV files")

        # Step 2: Directly fetch column reference files for identified CSV files
        logger.info(f"🔍 Fetching column references for identified files: {list(identified_filenames)}")
        column_docs = []

        # Try multiple search approaches to ensure we get column references
        try:
            # Approach 1: Search for all column reference files
            all_column_docs = vectorstore.similarity_search(
                "column names reference format",
                k=10,
                filter={"knowledge_path": "column_references"}
            )
            logger.info(f"📋 Found {len(all_column_docs)} total column reference docs")

            # Match them to our identified files
            for md_filename in identified_filenames:
                if md_filename != 'Unknown':
                    base_name = md_filename.replace('.md', '')
                    column_filename = f"{base_name}_columns.md"

                    # Find docs for this specific file
                    file_docs = [doc for doc in all_column_docs if doc.metadata.get('filename') == column_filename]
                    column_docs.extend(file_docs)
                    logger.info(f"📋 Found {len(file_docs)} column docs for {column_filename}")

        except Exception as e:
            logger.warning(f"⚠️ Column reference search failed: {e}")
            # Fallback: Search without filter
            try:
                fallback_docs = vectorstore.similarity_search("column names reference", k=10)
                column_docs = [doc for doc in fallback_docs if "column_references" in doc.metadata.get('folder', '')]
                logger.info(f"📋 Fallback found {len(column_docs)} column docs")
            except Exception as e2:
                logger.warning(f"⚠️ Fallback column search also failed: {e2}")

        logger.info(f"📋 Total column reference sections found: {len(column_docs)}")

        context_string = ""

        for file_idx, (filename, content_chunks) in enumerate(files_content.items(), 1):
            csv_path = f"docs/csvs/{filename}"
            md_filename = filename.replace('.csv', '.md')

            # Create clear file separator
            file_separator = f"\n{'='*80}\n📄 FILE {file_idx}: {filename}\n📍 PATH: {csv_path}\n{'='*80}"
            context_string += file_separator

            # Add column references first for this file
            column_filename = f"{filename.replace('.csv', '')}_columns.md"
            file_column_docs = [doc for doc in column_docs if doc.metadata.get('filename') == column_filename]
            if file_column_docs:
                context_string += f"\n--- COLUMN REFERENCES for {filename} ---\n"
                for col_doc in file_column_docs:
                    context_string += f"{col_doc.page_content}\n"
                context_string += f"--- END COLUMN REFERENCES ---\n"

            # Add all content chunks for this file
            for chunk_idx, content in enumerate(content_chunks, 1):
                chunk_section = f"\n--- SECTION {chunk_idx} of {filename} ---\n{content}\n"
                context_string += chunk_section

            # Add file end separator
            file_end = f"\n{'='*80}\n🔚 END OF {filename}\n{'='*80}\n"
            context_string += file_end
        # Generate pandas code
        code = _generate_analysis_code(query, context_string)

        # Execute code safely
        success, result = _execute_code_safely(code)

        if success:
            logger.info("✅ CSV analysis completed successfully")
            final_result = f"**Analysis Results:**\n```\n{result}\n```"
            logger.info(f"📤 Final result returned to user:\n{final_result}")
            return final_result
        else:
            logger.error(f"❌ Code execution failed: {result}")
            error_result = f"Sorry, I encountered an error analyzing the data: {result}"
            logger.info(f"📤 Error result returned to user:\n{error_result}")
            return error_result

    except Exception as e:
        logger.error(f"❌ CSV analysis error: {e}")
        return f"Error analyzing CSV data: {str(e)}"


def _generate_analysis_code(query: str, context) -> str:
    """Generate pandas code for CSV analysis."""
    # Prepare file info
    prompt = f"""
    Context - {context}
    User Query - {query}

    Requirements:
    - Use pandas to load CSV from docs/csvs/ path
    - Always print() results clearly with labels
    - Use exact column names from context

    Generate ONLY executable Python code:
"""

    logger.info(f"🤖 LLM Query sent (context: {len(context)} chars, query: {query})")
    logger.info(f"📤 Full LLM Query:\n{prompt}")

    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    response = llm.invoke(prompt)

    logger.info(f"🤖 LLM Response: {response.content}")

    # Extract code from response
    code = response.content
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()

    logger.info(f"🤖 Generated analysis code ({len(code)} chars):")
    logger.info(f"📝 Code to execute:\n{code}")
    return code


def _execute_code_safely(code: str) -> tuple[bool, str]:
    """Execute pandas code safely and return results."""
    try:
        logger.info(f"🔧 Starting code execution...")

        # Safe execution environment
        exec_globals = {
            "pd": pd,
            "print": print,
            "__builtins__": {
                "len": len,
                "str": str,
                "int": int,
                "float": float,
                "round": round,
                "sum": sum,
                "min": min,
                "max": max,
                "abs": abs,
                "sorted": sorted,
                "__import__": __import__,
                "open": open,
                "next": next,
                "enumerate": enumerate,
                "range": range,
                "list": list,
                "dict": dict,
                "tuple": tuple,
                "set": set,
            },
        }

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()

        try:
            logger.info(f"🔧 Executing code in safe environment...")
            exec(code, exec_globals)
            sys.stdout = old_stdout
            output = captured_output.getvalue()

            logger.info(f"✅ Code execution completed successfully")
            logger.info(f"📤 Execution output:\n{output}")

            if output.strip():
                return True, output
            else:
                logger.warning("⚠️ Code executed but produced no output")
                return False, "Code executed but produced no output"

        finally:
            sys.stdout = old_stdout

    except Exception as e:
        error_msg = f"Execution error: {str(e)}"
        logger.error(f"❌ Code execution failed: {error_msg}")
        logger.error(f"❌ Exception type: {type(e).__name__}")

        # Log traceback for debugging
        import traceback
        logger.error(f"❌ Full traceback:\n{traceback.format_exc()}")

        return False, error_msg


def create_csv_analyzer_tool() -> Tool:
    """Create CSV analyzer tool."""
    return Tool(
        name="analyze_csv_data",
        description="Analyze CSV data to answer user questions about booking forms, pickup forms, purchase orders, delivery dates, vendor information, OTIF metrics, and other business data. Use for data queries like counts, lists, analysis, and specific records. IMPORTANT: Pass the user's complete question including what specific information they want to find. Do not truncate or summarize the user's request.",
        func=analyze_csv_data,
    )