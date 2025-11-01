import streamlit as st
import base64

import streamlit as st
import base64

def footer():
    st.markdown("""
        <style>
        .footer-container {
            background: #f6faf6;
            border: 1px solid #e3ede3;
            border-radius: 10px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.05);
            padding: 1.2rem 2rem;
            text-align: center;
            width: 80%;
            margin: 4rem auto 2rem auto;
            color: #333;
        }
        .footer-container strong {
            color: #2e7d32;
        }
        .footer-links a {
            color: #388e3c;
            text-decoration: none;
            margin: 0 0.8rem;
            font-weight: 500;
        }
        .footer-links a:hover {
            color: #1b5e20;
        }
        </style>

        <div class="footer-container">
            <p>🌿 <strong>GreenTech Solutions Rhône</strong> — Projet réalisé dans le cadre de l'analyse de données énergétiques</p>
            <small>© 2025 - Tous droits réservés</small>
            <div class="footer-links" style="margin-top: 0.5rem;">
                <a href="https://github.com/votre-projet" target="_blank">GitHub</a> |
                <a href="#">Contact</a> |
                <a href="#">Documentation</a>
            </div>
        </div>
    """, unsafe_allow_html=True)


@st.cache_data    
def get_image_base64(image_path):
    """Convertir une image en base64 pour l'afficher dans du HTML"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

def show():
    # En-tête principal
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
            padding: 3rem 2rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 2rem;
        ">
            <h1 style="color:white; font-size:48px; margin-bottom: 0.5rem;">
                🌿  GreenTech Solutions Rhône
            </h1>
            <p style="color:white; font-size:20px; opacity: 0.95; margin: 0;">
                Plateforme d'analyse de la performance énergétique des bâtiments
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Section Bienvenue
    st.markdown("##  Bienvenue !")
    
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 10px; border-left: 5px solid #6B8E23; margin-bottom: 2rem;">
        <p style="font-size: 18px; line-height: 1.8; color: #333;">
            Nous sommes ravis de vous accueillir sur <strong>GreenTech Solutions Rhône</strong>, une application interactive 
            dédiée à l'analyse et à la visualisation des performances énergétiques des logements de la région Rhône-Alpes.
            Notre objectif est de rendre les données énergétiques accessibles et compréhensibles pour tous.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section Objectifs
    st.markdown("##  Objectifs du projet")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #e8f5e9; padding: 1.5rem; border-radius: 10px; height: 100%;">
            <h4 style="color: #2e7d32;"> Visualisation des données</h4>
            <p>Transformer les données brutes de diagnostic de performance énergétique (DPE) en visualisations 
            interactives et compréhensibles pour faciliter la prise de décision.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #fff3e0; padding: 1.5rem; border-radius: 10px; height: 100%;">
            <h4 style="color: #f57c00;"> Sensibilisation énergétique</h4>
            <p>Sensibiliser les citoyens et les professionnels aux enjeux de la transition énergétique 
            en rendant visible l'impact de la consommation énergétique des bâtiments.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div style="background: #e3f2fd; padding: 1.5rem; border-radius: 10px; height: 100%;">
            <h4 style="color: #1976d2;"> Comparaison facilitée</h4>
            <p>Permettre aux utilisateurs de comparer facilement différents logements pour identifier 
            les opportunités d'économies d'énergie et de réduction d'émissions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: #f3e5f5; padding: 1.5rem; border-radius: 10px; height: 100%;">
            <h4 style="color: #7b1fa2;"> Prédiction intelligente</h4>
            <p>Développer des modèles de machine learning pour prédire la performance énergétique 
            et aider à la planification de rénovations énergétiques.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Section Sources de données
    st.markdown("##  Sources de données")
    
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <p style="font-size: 16px; line-height: 1.8; color: #555;">
            Notre application exploite des données publiques de qualité provenant de sources officielles :
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 15px; color: white; height: 280px;">
            <h3> ADEME</h3>
            <h5>Agence de la transition écologique</h5>
            <p style="margin-top: 1rem; line-height: 1.6;">
                <strong>Données DPE (Diagnostic de Performance Énergétique)</strong><br><br>
                ✓ Consommation énergétique par logement<br>
                ✓ Émissions de gaz à effet de serre<br>
                ✓ Étiquettes énergétiques (A à G)<br>
                ✓ Caractéristiques techniques des bâtiments
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #f5f5f5; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #667eea;">
            <p style="margin: 0; color: #555;">
                <strong> API ADEME :</strong> 
                <a href="https://data.ademe.fr/" target="_blank" style="color: #667eea;">data.ademe.fr</a><br>
                <small>Base de données publique des DPE en France</small>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 2rem; border-radius: 15px; color: white; height: 280px;">
            <h3> Enedis</h3>
            <h5>Gestionnaire du réseau électrique</h5>
            <p style="margin-top: 1rem; line-height: 1.6;">
                <strong>Données de consommation électrique</strong><br><br>
                ✓ Consommation électrique régionale<br>
                ✓ Données temporelles et géographiques<br>
                ✓ Profils de consommation<br>
                ✓ Statistiques par secteur
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #f5f5f5; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #f5576c;">
            <p style="margin: 0; color: #555;">
                <strong> API Enedis :</strong> 
                <a href="https://data.enedis.fr/" target="_blank" style="color: #f5576c;">data.enedis.fr</a><br>
                <small>Open Data du distributeur d'électricité</small>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Section Équipe
    st.markdown("##  L'équipe du projet")
    
    st.markdown("""
    <p style="text-align: center; font-size: 18px; color: #666; margin-bottom: 2rem;">
        Rencontrez les développeurs passionnés derrière EcoVision Rhône
    </p>
    """, unsafe_allow_html=True)
    
    # Exemple d'équipe - À personnaliser avec tes vraies informations
    col1, col2, col3 = st.columns(3)
    
    # Charger les images en base64
    img_nico = get_image_base64("assets/nico_profile.jpeg")
    img_noro = get_image_base64("assets/rina.png")
    img_modou = get_image_base64("assets/modou_profile.jpeg")
    
    with col1:
        # Afficher l'image ou un placeholder si elle n'existe pas
        if img_nico:
            img_html = f'<img src="data:image/jpeg;base64,{img_nico}" style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover;">'
        else:
            img_html = '<span style="font-size: 48px;"></span>'
        
        st.markdown(f"""
        <div style="background: white; padding: 2rem; border-radius: 15px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;">
            <div style="width: 120px; height: 120px; border-radius: 50%; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        margin: 0 auto 1rem auto; display: flex; align-items: center; justify-content: center;">
                {img_html}
            </div>
            <h4 style="margin: 1rem 0 0.5rem 0; color: #333;">Nico DENA</h4>
            <p style="color: #666; margin: 0.5rem 0;">Data Scientist</p>
            <hr style="margin: 1rem 0; border: none; border-top: 1px solid #eee;">
            <p style="margin: 0.5rem 0;">
                <a href="mailto:franckdena@gmail.com" style="color: #667eea; text-decoration: none;">
                     franckdena@gmail.com
                </a>
            </p>
            <p style="margin: 0.5rem 0;">
                <a href="https://github.com/Denanico1" target="_blank" style="color: #333; text-decoration: none;">
                     github.com/Denanico1
                </a>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Afficher l'image ou un placeholder si elle n'existe pas
        if img_noro:
            img_html = f'<img src="data:image/jpeg;base64,{img_noro}" style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover;">'
        else:
            img_html = '<span style="font-size: 48px;"></span>'
        
        st.markdown(f"""
        <div style="background: white; padding: 2rem; border-radius: 15px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;">
            <div style="width: 120px; height: 120px; border-radius: 50%; 
                        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                        margin: 0 auto 1rem auto; display: flex; align-items: center; justify-content: center;">
                {img_html}
            </div>
            <h4 style="margin: 1rem 0 0.5rem 0; color: #333;">Noro Razafimahefa</h4>
            <p style="color: #666; margin: 0.5rem 0;">Data Scientist</p>
            <hr style="margin: 1rem 0; border: none; border-top: 1px solid #eee;">
            <p style="margin: 0.5rem 0;">
                <a href="mailto:n.razafimahefa@univ-lyon2.fr" style="color: #667eea; text-decoration: none;">
                     n.razafimahefa@univ-lyon2.fr
                </a>
            </p>
            <p style="margin: 0.5rem 0;">
                <a href="https://github.com/rsquaredata" target="_blank" style="color: #333; text-decoration: none;">
                     github.com/rsquaredata
                </a>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Afficher l'image ou un placeholder si elle n'existe pas
        if img_modou:
            img_html = f'<img src="data:image/jpeg;base64,{img_modou}" style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover;">'
        else:
            img_html = '<span style="font-size: 48px;"></span>'
        
        st.markdown(f"""
        <div style="background: white; padding: 2rem; border-radius: 15px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;">
            <div style="width: 120px; height: 120px; border-radius: 50%; 
                        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                        margin: 0 auto 1rem auto; display: flex; align-items: center; justify-content: center;">
                {img_html}
            </div>
            <h4 style="margin: 1rem 0 0.5rem 0; color: #333;">MBOUP Modou</h4>
            <p style="color: #666; margin: 0.5rem 0;">Data Scientist</p>
            <hr style="margin: 1rem 0; border: none; border-top: 1px solid #eee;">
            <p style="margin: 0.5rem 0;">
                <a href="mailto:mboupmodou05@gmail.com" style="color: #4facfe; text-decoration: none;">
                     m.mboup@univ-lyon2.fr
                </a>
            </p>
            <p style="margin: 0.5rem 0;">
                <a href="https://github.com/modou010" target="_blank" style="color: #333; text-decoration: none;">
                     github.com/modou010
                </a>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Section Technologies
    st.markdown("##  Technologies utilisées")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 48px; margin-bottom: 0.5rem;"></div>
            <strong>Python</strong><br>
            <small>Langage principal</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 48px; margin-bottom: 0.5rem;"></div>
            <strong>Streamlit</strong><br>
            <small>Interface web</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 48px; margin-bottom: 0.5rem;"></div>
            <strong>Plotly</strong><br>
            <small>Visualisations</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 48px; margin-bottom: 0.5rem;"></div>
            <strong>Scikit-learn</strong><br>
            <small>Machine Learning</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
