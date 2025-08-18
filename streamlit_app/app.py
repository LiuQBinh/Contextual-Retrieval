import streamlit as st
import os
from dotenv import load_dotenv
from contextual_retrieval import ContextualRetrieval, Reranker

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Contextual Retrieval Experiment",
    page_icon="🔍",
    layout="wide"
)

# Title
st.title("🔍 Contextual Retrieval Experiment")
st.markdown("Real-world Contextual Retrieval experiment based on Anthropic's paper")

# Sidebar configuration
st.sidebar.header("⚙️ Configuration")

# LM Studio URL
lm_studio_url = st.sidebar.text_input(
    "LM Studio URL",
    value="http://localhost:1234/v1",
    help="URL of LM Studio server"
)

# Qdrant URL
qdrant_url = st.sidebar.text_input(
    "Qdrant URL",
    value="http://localhost:6333",
    help="URL of Qdrant server"
)

# Chunk size
chunk_size = st.sidebar.slider(
    "Chunk Size",
    min_value=200,
    max_value=2000,
    value=800,
    step=100,
    help="Size of each chunk"
)

# Chunk overlap
chunk_overlap = st.sidebar.slider(
    "Chunk Overlap",
    min_value=0,
    max_value=500,
    value=200,
    step=50,
    help="Overlap between chunks"
)

# Top K results
top_k = st.sidebar.slider(
    "Top K Results",
    min_value=5,
    max_value=50,
    value=20,
    step=5,
    help="Number of results to return"
)

# Main content
tab1, tab2, tab3 = st.tabs(["🚀 Setup & Build", "🔍 Search", "📊 Evaluation"])

with tab1:
    st.header("Setup & Build System")
    
    # PDF Directory
    pdf_directory = st.text_input(
        "PDF Directory Path",
        value="chunks",
        help="Path to directory containing PDF files"
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📚 Load Documents"):
            try:
                # Initialize system
                retrieval_system = ContextualRetrieval(
                    lm_studio_url=lm_studio_url,
                    qdrant_url=qdrant_url,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap
                )
                
                # Load documents
                retrieval_system.load_documents(pdf_directory)
                
                # Save to session state
                st.session_state.retrieval_system = retrieval_system
                st.success("✅ Documents loaded successfully!")
                
            except Exception as e:
                st.error(f"❌ Error loading documents: {e}")
    
    with col2:
        if st.button("✂️ Split Chunks"):
            if 'retrieval_system' in st.session_state:
                try:
                    retrieval_system = st.session_state.retrieval_system
                    retrieval_system.split_documents()
                    st.success("✅ Documents split into chunks!")
                except Exception as e:
                    st.error(f"❌ Error splitting documents: {e}")
            else:
                st.warning("⚠️ Please load documents first!")
    
    with col3:
        if st.button("🧠 Generate Context"):
            if 'retrieval_system' in st.session_state:
                try:
                    retrieval_system = st.session_state.retrieval_system
                    
                    # Progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Generate context
                    retrieval_system.contextualize_chunks()
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Context generation completed!")
                    st.success("✅ Context generated for all chunks!")
                    
                except Exception as e:
                    st.error(f"❌ Error generating context: {e}")
            else:
                st.warning("⚠️ Please load and split documents first!")
    
    # Build indices
    st.subheader("Build Search Indices")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Build BM25 Index"):
            if 'retrieval_system' in st.session_state:
                try:
                    retrieval_system = st.session_state.retrieval_system
                    retrieval_system.build_bm25_index(use_context=True)
                    st.success("✅ BM25 index built!")
                except Exception as e:
                    st.error(f"❌ Error building BM25 index: {e}")
            else:
                st.warning("⚠️ Please load documents first!")
    
    with col2:
        if st.button("🗄️ Build Vector Store"):
            if 'retrieval_system' in st.session_state:
                try:
                    retrieval_system = st.session_state.retrieval_system
                    retrieval_system.build_vector_store(use_context=True)
                    st.success("✅ Vector store built!")
                except Exception as e:
                    st.error(f"❌ Error building vector store: {e}")
            else:
                st.warning("⚠️ Please load documents first!")
    
    # Save system
    if st.button("💾 Save System"):
        if 'retrieval_system' in st.session_state:
            try:
                retrieval_system = st.session_state.retrieval_system
                retrieval_system.save_system("saved_system")
                st.success("✅ System saved successfully!")
            except Exception as e:
                st.error(f"❌ Error saving system: {e}")
        else:
            st.warning("⚠️ Please build the system first!")

with tab2:
    st.header("Search & Retrieve")
    
    # Load saved system
    if st.button("📂 Load Saved System"):
        try:
            retrieval_system = ContextualRetrieval(
                lm_studio_url=lm_studio_url,
                qdrant_url=qdrant_url,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            retrieval_system.load_system("saved_system")
            st.session_state.retrieval_system = retrieval_system
            st.success("✅ System loaded successfully!")
        except Exception as e:
            st.error(f"❌ Error loading system: {e}")
    
    # Search interface
    if 'retrieval_system' in st.session_state:
        st.subheader("Search Query")
        
        query = st.text_area(
            "Enter your search query:",
            placeholder="Enter your question or search keywords...",
            height=100
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            use_context = st.checkbox("Use Contextual Retrieval", value=True)
            use_reranking = st.checkbox("Use Reranking", value=False)
        
        with col2:
            if st.button("🔍 Search", type="primary"):
                if query.strip():
                    try:
                        retrieval_system = st.session_state.retrieval_system
                        
                        # Perform search
                        results = retrieval_system.retrieve_hybrid(
                            query=query,
                            top_k=top_k,
                            use_context=use_context
                        )
                        
                        # Apply reranking if requested
                        if use_reranking:
                            reranker = Reranker(lm_studio_url=lm_studio_url)
                            results = reranker.rerank(query, results, top_k=top_k)
                        
                        # Display results
                        st.subheader(f"📋 Search Results ({len(results)} found)")
                        
                        for i, result in enumerate(results):
                            with st.expander(f"Result {i+1} - {result['method']} (Score: {result['score']:.4f})"):
                                st.markdown(f"**Source:** {result['chunk'].metadata.get('source', 'Unknown')}")
                                st.markdown(f"**Rank:** {result['rank']}")
                                st.markdown(f"**Method:** {result['method']}")
                                st.markdown("**Content:**")
                                st.text(result['chunk'].content[:1000] + "..." if len(result['chunk'].content) > 1000 else result['chunk'].content)
                    except Exception as e:
                        st.error(f"❌ Error performing search: {e}")
                else:
                    st.warning("⚠️ Please enter a search query")
    else:
        st.info("ℹ️ Please load or build the system first!")

with tab3:
    st.header("Evaluation & Comparison")
    
    if 'retrieval_system' in st.session_state:
        st.subheader("Compare Different Methods")
        
        # Test queries
        test_queries = [
            "What is the meaning of suffering?",
            "How to achieve enlightenment?",
            "What are the four noble truths?",
            "Explain the eightfold path",
            "What is karma in Buddhism?"
        ]
        
        selected_query = st.selectbox("Select test query:", test_queries)
        
        if st.button("📊 Run Comparison"):
            try:
                retrieval_system = st.session_state.retrieval_system
                
                # Test different methods
                methods = {
                    "Standard Retrieval": False,
                    "Contextual Retrieval": True
                }
                
                results_comparison = {}
                
                for method_name, use_context in methods.items():
                    results = retrieval_system.retrieve_hybrid(
                        query=selected_query,
                        top_k=top_k,
                        use_context=use_context
                    )
                    results_comparison[method_name] = results
                
                # Display comparison
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Standard Retrieval")
                    for i, result in enumerate(results_comparison["Standard Retrieval"][:5]):
                        st.markdown(f"**{i+1}.** {result['chunk'].content[:100]}...")
                
                with col2:
                    st.subheader("Contextual Retrieval")
                    for i, result in enumerate(results_comparison["Contextual Retrieval"][:5]):
                        st.markdown(f"**{i+1}.** {result['chunk'].content[:100]}...")
                
                # Metrics
                st.subheader("📈 Performance Metrics")
                
                # Calculate some basic metrics
                metrics_data = {
                    "Method": [],
                    "Avg Score": [],
                    "Unique Sources": []
                }
                
                for method_name, results in results_comparison.items():
                    avg_score = sum(r['score'] for r in results) / len(results) if results else 0
                    unique_sources = len(set(r['chunk'].metadata.get('source', '') for r in results))
                    
                    metrics_data["Method"].append(method_name)
                    metrics_data["Avg Score"].append(avg_score)
                    metrics_data["Unique Sources"].append(unique_sources)
                
                import pandas as pd
                metrics_df = pd.DataFrame(metrics_data)
                st.dataframe(metrics_df)
                
            except Exception as e:
                st.error(f"❌ Error running comparison: {e}")
    else:
        st.info("ℹ️ Please load or build the system first!")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, LM Studio, and Qdrant")
