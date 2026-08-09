from supabase import create_client, Client
from datetime import datetime, timedelta, UTC

# --- CONFIGURAÇÃO ---
SUPABASE_URL = "https://cfetiehlozifchyunbts.supabase.co"
SUPABASE_KEY = "sb_publishable_o-j5PbtgnZtXP73KnKhJzA_e_J9CM7-"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def buscar_historico(pena_id, cliente_id):
    limite_tempo = (datetime.now(UTC) - timedelta(hours=1)).isoformat()
    try:

        res = supabase.table("leituras_cloud").select("valor, timestamp_local").eq("pena_id", pena_id).eq("cliente_id", cliente_id).gte("created_at", limite_tempo).order("created_at", desc=False).execute()
        return res.data
    except:
        return []