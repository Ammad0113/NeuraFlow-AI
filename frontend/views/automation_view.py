import streamlit as st
from frontend.api_client import APIClient

def render_automation_view():
    st.markdown('<div class="nf-title">Python Automation Center</div>', unsafe_allow_html=True)
    st.markdown('<div class="nf-subtitle">Automate Folder Organization, Batch File Renaming, PDF Merging/Splitting & Task Log Tracking</div>', unsafe_allow_html=True)

    token = st.session_state.get("token")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Folder Organization", "Batch File Renaming", "PDF Merge & Split", "Automation Audit Log"
    ])

    with tab1:
        st.subheader("Automated Folder Organizer")
        st.caption("Sorts messy directory files into categorized subfolders (Documents, Images, Spreadsheets, Archives).")
        dir_path = st.text_input("Target Directory Path (e.g. C:\\Users\\LOQ\\Downloads)", key="org_path")
        
        if st.button("Run Folder Organizer", use_container_width=True, key="btn_org"):
            if not dir_path:
                st.warning("Please enter a valid directory path.")
            else:
                res = APIClient.post("/automation/organize-folder", json={"directory_path": dir_path}, token=token)
                if res.status_code == 200 and res.json().get("status") == "Success":
                    st.success(f"Organized {res.json()['moved_files']} files successfully!")
                else:
                    st.error(res.json().get("message", "Failed to organize directory."))

    with tab2:
        st.subheader("Batch File Renamer")
        rename_dir = st.text_input("Target Directory Path", key="ren_path")
        prefix = st.text_input("Filename Prefix", value="Enterprise_Doc", key="ren_prefix")
        ext_filter = st.text_input("Filter Extension (Optional, e.g. .pdf)", key="ren_ext")

        if st.button("Execute Batch Renaming", use_container_width=True, key="btn_ren"):
            res = APIClient.post("/automation/batch-rename", json={
                "directory_path": rename_dir, "prefix": prefix, "extension_filter": ext_filter if ext_filter else None
            }, token=token)
            if res.status_code == 200 and res.json().get("status") == "Success":
                st.success(f"Renamed {res.json()['renamed_files']} file(s)!")
            else:
                st.error(res.json().get("message", "Failed to execute batch renaming."))

    with tab3:
        st.subheader("Batch PDF Merger")
        pdf_files = st.file_uploader("Select Multiple PDFs to Merge", type=["pdf"], accept_multiple_files=True)
        
        if pdf_files and st.button("Merge Selected PDFs", use_container_width=True, key="btn_merge"):
            files_payload = [("files", (f.name, f.getvalue(), "application/pdf")) for f in pdf_files]
            res_m = APIClient.post("/automation/pdf-merge", files=files_payload, token=token)
            if res_m.status_code == 200:
                st.download_button(
                    label="Download Merged PDF Document",
                    data=res_m.content,
                    file_name="merged_documents.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                st.success("PDFs merged successfully!")
            else:
                st.error("Failed to merge PDFs.")

    with tab4:
        st.subheader("Execution History & Audit Trail")
        res_h = APIClient.get("/automation/history", token=token)
        logs = res_h.json() if res_h.status_code == 200 else []
        
        if logs:
            for l in logs:
                st.markdown(f"**{l['task_name']}** — <span style='color:#34D399;'>[{l['status']}]</span> ({l['created_at'][:19]})", unsafe_allow_html=True)
                st.caption(l["result_summary"])
                st.markdown("<hr style='border-color:rgba(255,255,255,0.08); margin:0.3rem 0;' />", unsafe_allow_html=True)
        else:
            st.caption("No automation tasks executed yet.")
