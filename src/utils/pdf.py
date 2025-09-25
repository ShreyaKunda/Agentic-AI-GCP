

import streamlit 
as st

import pandas 
as pd



# Page configuration

st.set_page_config(

    page_title="DMA Attacks & PCIe Security Report",

    page_icon="🔒",

    layout="wide",

    initial_sidebar_state="expanded"

)



# Custom CSS for better styling

st.markdown("""

<style>

.main-header {

    font-size: 2.5rem;

    color: #1e3a8a;

    text-align: center;

    margin-bottom: 2rem;

}

.section-header {

    color: #dc2626;

    border-bottom: 2px solid #dc2626;

    padding-bottom: 0.5rem;

    margin: 2rem 0 1rem 0;

}

.subsection-header {

    color: #059669;

    margin: 1.5rem 0 0.5rem 0;

}

.attack-box {

    background-color: #fef2f2;

    border-left: 4px solid #dc2626;

    padding: 1rem;

    margin: 1rem 0;

}

.mitigation-box {

    background-color: #f0fdf4;

    border-left: 4px solid #059669;

    padding: 1rem;

    margin: 1rem 0;

}

.code-box {

    background-color: #1f2937;

    color: #f9fafb;

    padding: 1rem;

    border-radius: 0.5rem;

    font-family: 'Courier New', monospace;

}

</style>

""", 
unsafe_allow_html=True)



# Sidebar navigation

st.sidebar.title("Navigation")

sections = [

    "Overview",

    "Section 1: Black Hat DMA Attacks",

    "Section 2: PCIe Device Security Evolution",

    "Section 3: MemProcFS & PCILeech",

    "Comparison & Key Takeaways"

]



selected_section = st.sidebar.selectbox("Select Section", sections)



# Main header

st.markdown('<h1 class="main-header">🔒 DMA Attacks and PCIe Device Security</h1>',
unsafe_allow_html=True)

st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #6b7280;">Comprehensive Technical Report</p>',
unsafe_allow_html=True)



# Overview Section

if selected_section 
== "Overview":

    st.markdown('<h2 class="section-header">📋 Report Overview</h2>',
unsafe_allow_html=True)

    

    col1, col2, col3 = st.columns(3)

    

    with col1:

        st.metric("Sections Covered",
"3", 
"Research Areas")

    

    with col2:

        st.metric("Attack Vectors",
"5+", 
"DMA Techniques")

    

    with col3:

        st.metric("Mitigation Strategies",
"10+", 
"Protection Methods")

    

    st.markdown("""

    This technical report examines the current state of Direct Memory Access (DMA) attacks and PCIe device security.

    The report covers three major research areas:

    

    1. **Advanced DMA Attacks (Black Hat)** - Modern techniques to bypass OS security

    2. **PCIe Security Evolution** - Historical development and new attack surfaces  

    3. **Forensic Tools** - MemProcFS and PCILeech for security research

    

    ### Key Findings

    - DMA attacks remain highly effective against modern systems

    - IOMMU protections are often misconfigured or incomplete

    - Hardware-level cooperation is essential for effective mitigation

    """)



# Section 1: Black Hat DMA Attacks

elif selected_section 
== "Section 1: Black Hat DMA Attacks":

    st.markdown('<h2 class="section-header">⚡ Taking DMA Attacks to the Next Level</h2>',
unsafe_allow_html=True)

    

    # Attack Overview

    st.markdown('<div class="attack-box">',
unsafe_allow_html=True)

    st.markdown("""

    **🎯 Attack Summary**

    

    Modern DMA attacks can bypass sophisticated OS security mechanisms including:

    - Kernel integrity checks

    - IOMMU misconfigurations  

    - Virtualization boundaries

    """)

    st.markdown('</div>', 
unsafe_allow_html=True)

    

    # Target Environments

    st.markdown('<h3 class="subsection-header">🎯 Target Environments</h3>',
unsafe_allow_html=True)

    

    targets_data = {

        "Environment": ["Windows 10",
"Linux", 
"Virtualized"],

        "Security Feature": ["PatchGuard",
"KASLR", 
"VMware/Hyper-V"],

        "Bypass Status": ["✅ Bypassed",
"✅ Bypassed", 
"✅ Bypassed"]

    }

    st.dataframe(pd.DataFrame(targets_data), 
use_container_width=True)

    

    # Attack Workflow

    st.markdown('<h3 class="subsection-header">🔧 Implementation Workflow</h3>',
unsafe_allow_html=True)

    

    workflow_steps = [

        "**1. Prepare Hardware** - PCIe FPGA card or Thunderbolt expansion",

        "**2. Setup Software** - Load DMA attack tools (PCILeech)",

        "**3. Attack Execution** - Scan memory, modify structures, dump data",

        "**4. Persistence** - Optional payload injection for rootkits"

    ]

    

    for step 
in workflow_steps:

        st.markdown(f"-
{step}")

    

    # Command Examples

    st.markdown('<h3 class="subsection-header">💻 Command Examples</h3>',
unsafe_allow_html=True)

    

    st.code("""# Using PCILeech to dump memory over PCIe

pcileech dump -device fpga -out memory_dump.raw



# Searching for LSASS process in memory

pcileech kmd -device fpga -proc lsass.exe -action dump""",
language="bash")

    

    # Results

    st.markdown('<h3 class="subsection-header">📊 Attack Results</h3>',
unsafe_allow_html=True)

    

    col1, col2 = st.columns(2)

    

    with col1:

        st.markdown("""

        **Bypassed Protections:**

        - ✅ Kernel Patch Protection (PatchGuard)

        - ✅ SMEP (Supervisor Mode Execution Prevention)  

        - ✅ UEFI Secure Boot (runtime compromise)

        """)

    

    with col2:

        st.markdown("""

        **Performance Metrics:**

        - 📈 Memory reads > 1 GB/s over PCIe Gen2 x4

        - ⚡ 16 GB memory dump in seconds

        """)



# Section 2: PCIe Device Security Evolution  

elif selected_section 
== "Section 2: PCIe Device Security Evolution":

    st.markdown('<h2 class="section-header">🔄 Evolution of DMA Attacks</h2>',
unsafe_allow_html=True)

    

    # Timeline

    st.markdown('<h3 class="subsection-header">📅 Attack Timeline</h3>',
unsafe_allow_html=True)

    

    timeline_data = {

        "Year": ["2006",
"2012", 
"2016+"],

        "Technology": ["FireWire (IEEE 1394)",
"Thunderbolt", 
"PCIe Hot-plug + TB3"],

        "Attack Type": ["Memory access attacks",
"Thunderbolt-based attacks", 
"Hot-plug exploit chains"]

    }

    

    st.dataframe(pd.DataFrame(timeline_data), 
use_container_width=True)

    

    # New Attack Surfaces

    st.markdown('<h3 class="subsection-header">🎯 New Attack Surfaces</h3>',
unsafe_allow_html=True)

    

    attack_surfaces = [

        "**PCIe Hot-plug** with malicious devices",

        "**Pre-boot environments** (UEFI exploitation)",

        "**Firmware backdoor** implantation",

        "**Cryptographic material** exfiltration from RAM"

    ]

    

    for surface 
in attack_surfaces:

        st.markdown(f"-
{surface}")

    

    # Implementation Details

    st.markdown('<h3 class="subsection-header">⚙️ Implementation Workflow</h3>',
unsafe_allow_html=True)

    

    tabs = st.tabs(["Device Development",
"Memory Mapping", 
"Attack Execution", "Stealth/Evasion"])

    

    with tabs[0]:

        st.markdown("""

        **FPGA-based PCIe Endpoint**

        - Custom IP core for DMA read/write

        - Hardware-level memory access

        """)

    

    with tabs[1]:

        st.markdown("""

        **PCIe BAR Enumeration**

        - Map physical memory through bus master interface

        - Direct hardware memory access

        """)

    

    with tabs[2]:

        st.markdown("""

        **Payload Execution**

        - Dump credential caches and crypto keys

        - Inject payload into kernel/user space

        """)

    

    with tabs[3]:

        st.markdown("""

        **Evasion Techniques**

        - IOMMU bypass via misconfigured page tables

        - Exploit firmware bugs in BIOS/UEFI

        """)

    

    # Code Example

    st.markdown('<h3 class="subsection-header">💻 Code Example</h3>',
unsafe_allow_html=True)

    

    st.code("""// Example of PCIe DMA read transaction (pseudo-code)

dma_read(dst_buffer, physical_address, length);""",
language="c")



# Section 3: MemProcFS & PCILeech

elif selected_section 
== "Section 3: MemProcFS & PCILeech":

    st.markdown('<h2 class="section-header">🔍 Memory Forensics Tools</h2>',
unsafe_allow_html=True)

    

    # Tool Overview

    col1, col2 = st.columns(2)

    

    with col1:

        st.markdown("""

        ### MemProcFS

        - 📁 Mounts live memory as virtual filesystem

        - 🗂️ Provides `/processes`, `/modules`, `/handles`

        - 🔍 Easy navigation of kernel structures

        """)

    

    with col2:

        st.markdown("""

        ### PCILeech  

        - 🔌 Interfaces with FPGA/PCIe devices

        - 💾 Performs memory dumps via DMA

        - 🎯 Supports Windows, Linux, macOS

        """)

    

    # Supported Targets

    st.markdown('<h3 class="subsection-header">🎯 Supported Targets</h3>',
unsafe_allow_html=True)

    

    targets = ["Windows",
"Linux", 
"macOS", "Physical Machines", 
"Virtual Machines"]

    target_cols = st.columns(len(targets))

    

    for i, target 
in enumerate(targets):

        with target_cols[i]:

            st.success(f"✅
{target}")

    

    # Implementation Workflow

    st.markdown('<h3 class="subsection-header">⚙️ Implementation Steps</h3>',
unsafe_allow_html=True)

    

    st.markdown("""

    **1. Hardware Setup**

    - FPGA board with DMA firmware

    

    **2. Memory Acquisition** 

    """)

    

    st.code("pcileech fs -device fpga -vmmem winpmem",
language="bash")

    

    st.markdown("**3. Analysis**")

    st.code("""# Navigate processes

cd /processes



# Find lsass.exe

ls | grep lsass



# Dump memory

cp /memdump/lsass.dmp ./lsass_dump.dmp""",
language="bash")

    

    # Results & Capabilities

    st.markdown('<h3 class="subsection-header">📊 Results & Capabilities</h3>',
unsafe_allow_html=True)

    

    capabilities = [

        "🗂️ Entire memory mapped as filesystem",

        "🔍 Forensic analysis with no agent installation",

        "🛡️ Bypass anti-cheat solutions (BattlEye, PatchGuard)",

        "⚡ Real-time memory analysis"

    ]

    

    for capability 
in capabilities:

        st.markdown(f"-
{capability}")



# Comparison & Key Takeaways

elif selected_section 
== "Comparison & Key Takeaways":

    st.markdown('<h2 class="section-header">📋 Summary & Analysis</h2>',
unsafe_allow_html=True)

    

    # Comparison Table

    st.markdown('<h3 class="subsection-header">⚖️ Research Comparison</h3>',
unsafe_allow_html=True)

    

    comparison_data = {

        "Research": ["Black Hat DMA",
"PCIe Evolution", 
"MemProcFS/PCILeech"],

        "Focus": ["OS Bypass Techniques",
"Historical Analysis", 
"Forensic Tools"],

        "Primary Target": ["Modern OS Security",
"Hardware Evolution", 
"Memory Analysis"],

        "Key Tool": ["PCILeech",
"Custom FPGA", 
"MemProcFS"],

        "Difficulty": ["High",
"Medium", 
"Medium"]

    }

    

    st.dataframe(pd.DataFrame(comparison_data), 
use_container_width=True)

    

    # Key Takeaways

    st.markdown('<h3 class="subsection-header">🎯 Key Takeaways</h3>',
unsafe_allow_html=True)

    

    takeaway1, takeaway2, takeaway3 = st.columns(3)

    

    with takeaway1:

        st.markdown('<div class="attack-box">',
unsafe_allow_html=True)

        st.markdown("""

        **🚨 Still Relevant**

        

        DMA attacks remain highly effective in 2025. Hardware protections like IOMMU are often improperly configured.

        """)

        st.markdown('</div>', 
unsafe_allow_html=True)

    

    with takeaway2:

        st.markdown('<div class="attack-box">',
unsafe_allow_html=True)

        st.markdown("""

        **🛠️ Powerful Tools**

        

        PCILeech + MemProcFS provide red teamers and defenders with sophisticated capabilities for both attack and forensics.

        """)

        st.markdown('</div>', 
unsafe_allow_html=True)

    

    with takeaway3:

        st.markdown('<div class="attack-box">',
unsafe_allow_html=True)

        st.markdown("""

        **🔒 Complex Mitigation**

        

        Effective protection requires cooperation between BIOS, OS, and hardware-level security features.

        """)

        st.markdown('</div>', 
unsafe_allow_html=True)

    

    # Mitigation Summary

    st.markdown('<h3 class="subsection-header">🛡️ Consolidated Mitigation Strategies</h3>',
unsafe_allow_html=True)

    

    mitigation_categories = st.tabs(["Firmware/OS Level",
"Hardware Protections", 
"Operational Security"])

    

    with mitigation_categories[0]:

        st.markdown('<div class="mitigation-box">',
unsafe_allow_html=True)

        st.markdown("""

        - ✅ Enable and configure IOMMU properly (VT-d / AMD-Vi)

        - ✅ Enable DMA remapping in BIOS/UEFI

        - ✅ Enable Memory Access Protections (Windows 10 1803+)

        - ✅ Use encrypted memory (Intel TDX, AMD SEV-ES)

        """)

        st.markdown('</div>', 
unsafe_allow_html=True)

    

    with mitigation_categories[1]:

        st.markdown('<div class="mitigation-box">',
unsafe_allow_html=True)

        st.markdown("""

        - ✅ Use PCIe ACS (Access Control Services) isolation

        - ✅ Block unauthorized hot-plug PCIe devices

        - ✅ Set Thunderbolt Security Level 4

        - ✅ Fix ACS / ATS vulnerabilities

        """)

        st.markdown('</div>', 
unsafe_allow_html=True)

    

    with mitigation_categories[2]:

        st.markdown('<div class="mitigation-box">',
unsafe_allow_html=True)

        st.markdown("""

        - ✅ Disable unused ports

        - ✅ Monitor for suspicious PCIe enumeration events

        - ✅ Regular firmware updates

        - ✅ Physical security controls

        """)

        st.markdown('</div>', 
unsafe_allow_html=True)

    

    # Resources

    st.markdown('<h3 class="subsection-header">📚 References & Resources</h3>',
unsafe_allow_html=True)

    

    resources_data = {

        "Resource": [

            "Black Hat Video",

            "PCILeech GitHub", 

            "MemProcFS GitHub",

            "hardwear.io Video",

            "CS3STHLM Video"

        ],

        "Type": ["Video",
"Tool", 
"Tool", "Video", 
"Video"],

        "URL": [

            "https://www.youtube.com/watch?v=QeIPcA8zsHk",

            "https://github.com/ufrisk/pcileech",

            "https://github.com/ufrisk/MemProcFS",

            "https://www.youtube.com/watch?v=7nD391e_NK0",

            "https://www.youtube.com/watch?v=5DbQr3Zo-XY"

        ]

    }

    

    st.dataframe(pd.DataFrame(resources_data), 
use_container_width=True)



# Footer

st.markdown("---")

st.markdown("""

<div style='text-align: center; color: #6b7280; font-size: 0.9rem;'>

    <p>⚠️ This report is for educational and defensive security purposes only</p>

    <p>🔒 DMA Attacks & PCIe Device Security Technical Report</p>

</div>

""", 
unsafe_allow_html=True)

