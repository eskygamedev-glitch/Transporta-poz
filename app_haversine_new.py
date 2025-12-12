import requests
import time
import math


def fetch_data():
    response = requests.get(url, headers=headers)
    lines = response.text.split("\n")

    lines = [
        line for line in lines
        if any(line.startswith(seq) for seq in allowed_sequences)
    ]

    for line in lines:
        a = line.split(",")

        # parbaudei
        if len(a) < 5:
            continue

        vir = removeIntigers(a[8])

        # micro gradi
        lon_mikro = float(a[2])
        lat_mikro = float(a[3])

        # transporta veids
        def get_transport_name(value):
            if value == "1":
                return "Trolejbuss"
            elif value == "2":
                return "Autobuss"
            elif value == "3":
                return "Tramvajs"
            else:
                return "Nezināms transporta veids"

        transport = get_transport_name(a[0])

        # pareja
        lon = lon_mikro / 1000000
        lat = lat_mikro / 1000000

        # ATRAST TUVAKO/ESOŠO PIETURU — NOW PASSES a[0]
        pietura = trySearch(lat, lon, vir, a[0])
        
        if pietura is not None:
            print(
                f"==== {a[1]} {transport} ====\n"
                f"Pietura: {pietura}\n"
                f"Lat: {lat:.6f}\n"
                f"Lon: {lon:.6f}\n"
                f"Virziens: {vir}\n"
                f"================\n"
            )


url = "https://saraksti.lv/gpsdata.ashx?gps"
headers = {
    "Origin-Custom": "saraksti.lv"
}

def removeIntigers(vir):
    outputStr = ""
    for char in vir:
        if char in invalidChars:
            pass
        else:
            outputStr += char

    return outputStr

# parbaudei(vai ir pieturaa)
def haversine(lat1, lon1, lat2, lon2):
    R = 6363133  # Zemes radiuss(metros)
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# Atjauninata funkcija ar transport_id parametru
def trySearch(lat, lon, vir, transport_id):
    MAX_DISTANCE_METERS = 15
    closest_stop = None
    closest_distance = float("inf")

    # if route doesn't exist for this transport
    if transport_id not in ROUTES:
        return None

    stops = ROUTES[transport_id]  # ← SELECT CORRECT STOP LIST

    for stop in stops:
        stop_name, stop_lat, stop_lon, stop_way = stop
        distance = haversine(lat, lon, stop_lat, stop_lon)

        if distance < closest_distance and vir == stop_way:
            closest_distance = distance
            closest_stop = stop_name

    if closest_distance <= MAX_DISTANCE_METERS:
        #print(f"Atrasta atbilstība: {closest_stop} ({closest_distance:.1f} m attālumā)")
        return closest_stop
    else:
        return None


# All TRANSPORT LISTS
trol_3_stops = [
    ["sarkandaugava_station_bus_stop_a_b", 56.99569, 24.12903, "a-"],
    ["sarkandaugava_bus_stop_a_b", 56.99419, 24.12494, "a-"],
    ["sarkandaugava_bus_stop_b_a", 56.99487, 24.12679, "-a"],
    ["tilta_iela_bus_stop_b_a", 56.99232, 24.12559, "-a"],
    ["tilta_iela_bus_stop_a_b", 56.99287, 24.12413, "a-"],
    ["vitolu_iela_bus_stop_b_a", 56.99232, 24.12559, "-a"],
    ["vitolu_iela_bus_stop_a_b", 56.99287, 24.12413, "a-"],
    ["olaines_iela_bus_stop_b_a", 56.98653, 24.13385, "-a"],
    ["olaines_iela_bus_stop_a_b", 56.98733, 24.133, "a-"],
    ["traumatologijas_bus_stop_a_b", 56.98378, 24.13604, "a-"],
    ["traumatologijas_bus_stop_b_a", 56.98292, 24.13627, "-a"],
    ["laktas_iela_bus_stop_a_b", 56.97934, 24.13657, "a-"],
    ["laktas_iela_bus_stop_b_a", 56.9783, 24.13601, "-a"],
    ["ierednu_iela_bus_stop_a_b", 56.97434, 24.13557, "a-"],
    ["ierednu_iela_bus_stop_b_a", 56.97332, 24.13517, "-a"],
    ["eveles_iela_bus_stop_a_b", 56.97069, 24.1333, "a-"],
    ["eveles_iela_bus_stop_b_a", 56.96898, 24.13173, "-a"],
    ["palidzibas_iela_bus_stop_b_a", 56.96474, 24.12758, "-a"],
    ["bruninieku_iela_bus_stop_a_b", 56.96093, 24.1217, "a-"],
    ["bruninieku_iela_bus_stop_b_a", 56.96178, 24.12284, "-a"],
    ["emelngaila_iela_bus_stop_b_a", 56.95923, 24.11856, "-a"],
    ["raina_bulvaris_bus_stop_b_a", 56.95393, 24.10927, "2-a"],
    ["central_tirgus_bus_stop_a_b", 56.94572, 24.11878, "a-"],
    ["centrala_stacija_bus_stop_a_b", 56.94755, 24.11816, "a-"],
    ["centrala_stacija_bus_stop_b_a", 56.94607, 24.1187, "-a"],
    ["merkela_iela_bus_stop_a_b", 56.94908, 24.11928, "a-"],
    ["inzenieru_iela_bus_stop_a_b", 56.95122, 24.11682, "a-"],
    ["inzenieru_iela_bus_stop_b_a", 56.9509, 24.1149, "-a"],
    ["makslas_muzejs_bus_stop_a_b", 56.95565, 24.11133, "a-"],
    ["makslas_muzejs_bus_stop_b_a", 56.95611, 24.11258, "-a"],
    ["lacplesa_iela_bus_stop_a_b", 56.95818, 24.11688, "a-"],
    ["lacplesa_iela_bus_stop_b_a", 56.94978, 24.13127, "-a"],
    ["francu_licejs_bus_stopa_a_b", 56.96357, 24.12596, "a-"],
    ["aloju_iela_bus_stopa_a_b", 56.96757, 24.13079, "a-"],
]
bus_13_stops = [
    ["babites_stacija_a_b", 56.93017, 24.08835, "a-"],        # Torņakalna stacija area;
    ["spilve_a_b", 56.99789, 24.02935, "a-"],                 # Spilves pļavas
    ["mezāres_a_b", 56.98505, 24.02564, "a-"],                # Mikrobioloģijas institūts area
    ["pumpas_a_b", 56.98376, 24.03169, "a-"],                 # Pagrieziens uz Kleistiem area
    ["liepezers_a_b", 56.98686, 24.01407, "a-"],              # Kleisti
    ["kleisti_a_b", 56.98686, 24.01407, "a-"],
    ["mikrobiologijas_instituts_a_b", 56.98505, 24.02564, "a-"],
    ["pagrieziens_uz_kleistiem_a_b", 56.98376, 24.03169, "a-"],
    ["kleistu_iela_37_a_b", 56.97889, 24.03557, "a-"],
    ["gaili_a_b", 56.97606, 24.03511, "a-"],
    ["6_autobusu_parks_a_b", 56.97180, 24.03138, "a-"],
    ["melluzu_iela_a_b", 56.96666, 24.02697, "a-"],
    ["atc_latina_a_b", 56.96343, 24.03021, "a-"],
    ["observatorijas_iela_a_b", 56.95905, 24.06033, "a-"],     # nearest match Saldus iela area
    ["saulgozu_iela_a_b", 56.96132, 24.04769, "a-"],
    ["slokas_iela_a_b", 56.95204, 24.05391, "a-"],             # Botāniskais dārzs area
    ["vaidelotes_iela_a_b", 56.96121, 24.04849, "a-"],         # same pair
    ["bullu_iela_a_b", 56.95199, 24.04580, "a-"],              # Jūrmalas gatve area
    ["saldus_iela_a_b", 56.95905, 24.06033, "a-"],
    ["udens_iela_a_b", 56.95523, 24.06984, "a-"],
    ["klingeru_iela_a_b", 56.95332, 24.15537, "a-"],           # Daugavas stadions area
    ["kipsala_a_b", 56.95327, 24.10458, "a-"],                 # Nacionālais teātris + LU side
    ["nacionalais_teatris_a_b", 56.95375, 24.10419, "a-"],
    ["brivibas_bulvaris_a_b", 56.95175, 24.11617, "a-"],
    ["centrala_stacija_a_b", 56.94764, 24.11885, "a-"],
    ["dzirnavu_iela_a_b", 56.95071, 24.12542, "a-"],
    ["gertrudes_iela_a_b", 56.95676, 24.12194, "a-"],
    ["avotu_iela_a_b", 56.95345, 24.12987, "a-"],              # A.Čaka iela
    ["matisa_iela_a_b", 56.96029, 24.13050, "a-"],
    ["lienes_iela_a_b", 56.95365, 24.14774, "a-"],
    ["daugavas_stadions_a_b", 56.95332, 24.15537, "a-"],
    ["itas_kozakevicas_iela_a_b", 56.95016, 24.17311, "a-"],
    ["vietalvas_iela_a_b", 56.94544, 24.17202, "a-"],
    ["jaunrozes_iela_a_b", 56.94470, 24.16981, "a-"],
    ["rp_rigas_satiksme_a_b", 56.94365, 24.16486, "a-"],
    ["7_autobusu_parks_a_b", 56.94023, 24.16586, "a-"],
    ["piedrujas_iela_a_b", 56.93965, 24.17286, "a-"],
    ["pildas_iela_a_b", 56.94136, 24.18163, "a-"],
    ["strautu_iela_a_b", 56.93734, 24.18209, "a-"],
    ["slavu_aplis_darzc_iela_a_b", 56.93201, 24.18149, "a-"],
    ["slavu_aplis_lubanas_a_b", 56.93270, 24.18190, "a-"],
    ["ilukstes_iela_a_b", 56.93170, 24.19401, "a-"],
    ["katlakalna_iela_a_b", 56.93173, 24.20181, "a-"],
    ["cesvaines_iela_a_b", 56.93011, 24.21178, "a-"],
    ["rencenu_iela_a_b", 56.92275, 24.21275, "a-"],
    ["precu_2_a_b", 56.92250, 24.21707, "a-"],


    # B-A STOPS
    ["precu_2_b_a", 56.92250, 24.21707, "-a"],
    ["rencenu_iela_b_a", 56.92275, 24.21275, "-a"],
    ["jukuma_vaciesa_iela_b_a", 56.93158, 24.20996, "-a"],
    ["katlakalna_iela_b_a", 56.93203, 24.19866, "-a"],
    ["ilukstes_iela_b_a", 56.93170, 24.19401, "-a"],
    ["slavu_rotacijas_aplis_lubanas_iela_b_a", 56.93396, 24.19086, "-a"],
    ["slavu_rotacijas_aplis_darzciema_iela_b_a", 56.93482, 24.18894, "-a"],
    ["strautu_iela_b_a", 56.93189, 24.18114, "-a"],
    ["pildas_iela_b_a", 56.93146, 24.17868, "-a"],
    ["piedrujas_iela_b_a", 56.93192, 24.17437, "-a"],
    ["7_autobusu_parks_b_a", 56.93413, 24.17192, "-a"],
    ["rp_sia_rigas_satiksme_b_a", 56.93635, 24.16796, "-a"],
    ["vietalvas_iela_b_a", 56.93878, 24.16022, "-a"],
    ["itas_kozakevicas_iela_b_a", 56.94038, 24.15471, "-a"],
    ["daugavas_stadions_b_a", 56.94268, 24.15164, "-a"],
    ["lienes_iela_b_a", 56.94724, 24.13840, "-a"],
    ["bruninieku_iela_b_a", 56.95173, 24.13545, "-a"],
    ["stabu_iela_b_a", 56.95386, 24.13468, "-a"],
    ["gertrudes_iela_b_a", 56.95572, 24.13361, "-a"],
    ["dzirnavu_iela_b_a", 56.95794, 24.13292, "-a"],
    ["merkela_iela_b_a", 56.95193, 24.11963, "-a"],
    ["inzenieru_iela_b_a", 56.95090, 24.11490, "-a"],
    ["nacionalais_teatris_b_a", 56.95280, 24.11049, "-a"],
    ["kipsala_b_a", 56.95847, 24.08407, "-a"],
    ["klingeru_iela_b_a", 56.96360, 24.03632, "-a"],
    ["udens_iela_b_a", 56.96386, 24.03562, "-a"],
    ["saldus_iela_b_a", 56.96639, 24.03553, "-a"],
    ["dzirciema_iela_b_a", 56.96905, 24.03529, "-a"],
    ["vaidelotes_iela_b_a", 56.96073, 24.03928, "-a"],
    ["saulgozu_iela_b_a", 56.96163, 24.03971, "-a"],
    ["observatorijas_iela_b_a", 56.96187, 24.03932, "-a"],
    ["atc_latina_b_a", 56.96343, 24.03021, "-a"],
    ["melluzu_iela_b_a", 56.96666, 24.02697, "-a"],
    ["6_autobusu_parks_b_a", 56.97180, 24.03138, "-a"],
    ["gaili_b_a", 56.97606, 24.03511, "-a"],
    ["kleistu_iela_37_b_a", 56.97889, 24.03557, "-a"],
    ["pagrieziens_uz_kleistiem_b_a", 56.98431, 24.03281, "-a"],
    ["mikrobiologijas_instituts_b_a", 56.98505, 24.02564, "-a"],
    ["kleisti_b_a", 56.98686, 24.01407, "-a"],
    ["liepezers_b_a", 56.98439, 24.00135, "-a"],
    ["pumpas_b_a", 56.97838, 23.97450, "-a"],
    ["mezares_b_a", 56.97464, 23.96883, "-a"],
    ["spilve_b_a", 56.96453, 23.96273, "-a"],
    ["rododendru_audzetava_b_a", 56.95976, 23.95258, "-a"],
    ["babites_stacija_b_a", 56.95822, 23.95345, "-a"]
]
tram_11_stops = [
    #b-a direction
    ["ezermalas_iela_tram_stop_ba", 57.00685, 24.1642, "-a"],
    ["mezaparks_zoo_tram_stop_ba", 57.00469, 24.15705, "-a"],
    ["visbijas_prospekts_tram_stop_ba", 57.00055, 24.15951, "-a"],
    ["hamburgas_iela_tram_stop_ba", 56.99743, 24.16141, "-a"],
    ["mirdzas_kempes_iela_tram_stop_ba", 56.9937, 24.16366, "-a"],
    ["rusova_ielavalsts_ienemumu_dienests_tram_stop_ba", 56.98874, 24.16443, "-a"],
    ["gaujas_iela_tram_stop_ba", 56.98646, 24.16046, "-a"],
    ["2meza_kapi_tram_stop_ba", 56.98425, 24.1555, "-a"],
    ["bralu_kapi_tram_stop_ba", 56.98264, 24.15164, "-a"],
    ["brasas_stacija_tram_stop_ba", 56.97582, 24.14434, "-a"],
    ["kazarmu_ielalielie_kapi_tram_stop_ba", 56.9732, 24.14186, "-a"],
    ["meness_iela_tram_stop_ba", 56.96864, 24.1366, "-a"],
    ["dzemdibu_nams_tram_stop_ba", 56.96605, 24.13359, "-a"],
    ["laima_tram_stop_ba", 56.96356, 24.13188, "-a"],
    ["brivibas_iela_tram_stop_ba", 56.96305, 24.13597, "-a"],
    ["bernu_pasaule_tram_stop_ba", 56.9573, 24.1335, "-a"],
    ["gertrudes_iela_tram_stop_ba", 56.95359, 24.13146, "-a"],
    ["dzirnavu_iela_tram_stop_ba", 56.94891, 24.12561, "-a"],
    ["merkela_iela_tram_stop_ba", 56.94995, 24.11864, "-a"],
    ["aspazijas_bulvaris_tram_stop_ba", 56.94811, 24.11486, "-a"],
    ["nacionala_opera_tram_stop_ba", 56.94863, 24.11399, "-a"],
    ["nacionalais_teatris_tram_stop_ba", 56.95377, 24.10646, "-a"],
    ["ausekla_iela_tram_stop_ba", 56.95742, 24.10083, "-a"],
    #a-b direction
    ["ausekla_iela_tram_stop_aa", 56.95742, 24.10083, "a-"],
    ["nacionalais_teatris_tram_stop_aa", 56.95377, 24.10646, "a-"],
    ["nacionala_opera_tram_stop_aa", 56.94863, 24.11399, "a-"],
    ["merkela_iela_tram_stop_aa", 56.94995, 24.11864, "a-"],
    ["dzirnavu_iela_tram_stop_aa", 56.94891, 24.12561, "a-"],
    ["gertrudes_iela_tram_stop_aa", 56.95359, 24.13146, "a-"],
    ["bernu_pasaule_tram_stop_aa", 56.9573, 24.1335, "a-"],
    ["brivibas_iela_tram_stop_aa", 56.96305, 24.13597, "a-"],
    ["laima_tram_stop_aa", 56.96356, 24.13188, "a-"],
    ["dzemdibu_nams_tram_stop_aa", 56.96605, 24.13359, "a-"],
    ["meness_iela_tram_stop_aa", 56.96864, 24.1366, "a-"],
    ["kazarmu_ielalielie_kapi_tram_stop_aa", 56.9732, 24.14186, "a-"],
    ["brasas_stacija_tram_stop_aa", 56.97582, 24.14434, "a-"],
    ["bralu_kapi_tram_stop_aa", 56.98264, 24.15164, "a-"],
    ["2meza_kapi_tram_stop_aa", 56.98425, 24.1555, "a-"],
    ["gaujas_iela_tram_stop_aa", 56.98646, 24.16046, "a-"],
    ["rusova_ielavalsts_ienemumu_dienests_tram_stop_aa", 56.98874, 24.16443, "a-"],
    ["mirdzas_kempes_iela_tram_stop_aa", 56.9937, 24.16366, "a-"],
    ["hamburgas_iela_tram_stop_aa", 56.99743, 24.16141, "a-"],
    ["visbijas_prospekts_tram_stop_aa", 57.00055, 24.15951, "a-"],
    ["mezaparks_zoo_tram_stop_aa", 57.00469, 24.15705, "a-"],
    ["ezermalas_iela_tram_stop_aa", 57.00685, 24.1642, "a-"]
]
trol_5_stops = [
    #a-b
    ["daugavas_stadions_tram_stop_aa", 56.95328, 24.15477, "a-"],
    ["jasara_iela_tram_stop_aa", 56.95445, 24.15138, "a-"],
    ["varnu_iela_tram_stop_aa", 56.95926, 24.15202, "a-"],
    ["acaka_iela_tram_stop_aa", 56.95465, 24.13487, "a-"],
    ["kbarona_iela_tram_stop_aa", 56.96789, 24.14961, "a-"],
    ["brivibas_iela_tram_stop_aa", 56.96305, 24.13597, "a-"],
    ["dzemdibu_nams_tram_stop_aa", 56.96605, 24.13359, "a-"],
    ["francu_licejs_tram_stop_aa", 56.96291, 24.12541, "a-"],
    ["bruninieku_iela_tram_stop_aa", 56.95228, 24.14022, "a-"],
    ["emelngaila_iela_tram_stop_aa", 56.95923, 24.11856, "a-"],
    ["makslas_muzejs_tram_stop_aa", 56.95565, 24.11133, "a-"],
    ["nacionalais_teatris_tram_stop_aa", 56.95377, 24.10646, "a-"],
    ["kipsala_tram_stop_aa", 56.94991, 24.08708, "a-"],
    ["balozu_iela_tram_stop_aa", 56.94571, 24.07205, "a-"],
    ["melnsila_iela_tram_stop_aa", 56.94358, 24.06877, "a-"],
    ["vila_pludona_iela_tram_stop_aa", 56.94052, 24.07028, "a-"],
    ["nometnu_iela_tram_stop_aa", 56.9381, 24.07216, "a-"],
    ["agenskalna_tirgus_tram_stop_aa", 56.93569, 24.0724, "a-"],
    ["tukuma_iela_tram_stop_aa", 56.93293, 24.07164, "a-"],
    ["paula_stradina_slimnica_tram_stop_aa", 56.92968, 24.06534, "a-"],
    #b-a
    ["paula_stradina_slimnica_tram_stop_ba", 56.92968, 24.06534, "-a"],
    ["tukuma_iela_tram_stop_ba", 56.93293, 24.07164, "-a"],
    ["agenskalna_tirgus_tram_stop_ba", 56.93569, 24.0724, "-a"],
    ["vila_pludona_iela_tram_stop_ba", 56.94052, 24.07028, "-a"],
    ["kapselu_iela_tram_stop_ba", 56.94305, 24.0713, "-a"],
    ["valsts_arhivs_tram_stop_ba", 56.94647, 24.07532, "-a"],
    ["kipsala_tram_stop_ba", 56.94991, 24.08708, "-a"],
    ["nacionalais_teatris_tram_stop_ba", 56.95377, 24.10646, "-a"],
    ["makslas_muzejs_tram_stop_ba", 56.95565, 24.11133, "-a"],
    ["lacplesa_iela_tram_stop_ba", 56.94978, 24.13127, "-a"],
    ["bruninieku_iela_tram_stop_ba", 56.95228, 24.14022, "-a"],
    ["francu_licejs_tram_stop_ba", 56.96291, 24.12541, "-a"],
    ["dzemdibu_nams_tram_stop_ba", 56.96605, 24.13359, "-a"],
    ["brivibas_iela_tram_stop_ba", 56.96305, 24.13597, "-a"],
    ["kbarona_iela_tram_stop_ba", 56.96789, 24.14961, "-a"],
    ["acaka_iela_tram_stop_ba", 56.95465, 24.13487, "-a"],
    ["varnu_iela_tram_stop_ba", 56.95926, 24.15202, "-a"],
    ["jasara_iela_tram_stop_ba", 56.95445, 24.15138, "-a"],
    ["daugavas_stadions_tram_stop_ba", 56.95328, 24.15477, "-a"]
]
tram_7_stops = [
    # a-b
    ["ausekla_iela_tram_stop_aa", 56.95742, 24.10083, "a-"],
    ["nacionalais_teatris_tram_stop_aa", 56.95377, 24.10646, "a-"],
    ["nacionala_opera_tram_stop_aa", 56.94863, 24.11399, "a-"],
    ["centraltirgus_tram_stop_aa", 56.94411, 24.11433, "a-"],
    ["spikeri_tram_stop_aa", 56.94234, 24.11619, "a-"],
    ["jezusbaznicas_iela_tram_stop_aa", 56.94104, 24.1208, "a-"],
    ["elijas_iela_tram_stop_aa", 56.93988, 24.12574, "a-"],
    ["katolu_iela_tram_stop_aa", 56.93958, 24.13549, "a-"],
    ["daugavpils_iela_tram_stop_aa", 56.93898, 24.14004, "a-"],
    ["maza_kalna_iela_tram_stop_aa", 56.94232, 24.14533, "a-"],
    ["latgales_parks_tram_stop_aa", 56.93599, 24.15587, "a-"],
    ["reznas_iela_tram_stop_aa", 56.93341, 24.15995, "a-"],
    ["atputas_centrs_lido_tram_stop_aa", 56.92708, 24.15909, "a-"],
    ["krasta_masivs_tram_stop_aa", 56.92556, 24.16815, "a-"],
    ["dienvidu_tilts_tram_stop_aa", 56.92137, 24.17137, "a-"],
    ["kengaraga_iela_tram_stop_aa", 56.91887, 24.17329, "a-"],
    ["prusu_iela_tram_stop_aa", 56.91422, 24.17554, "a-"],
    ["rusonu_iela_tram_stop_aa", 56.91067, 24.17951, "a-"],
    ["malnavas_iela_tram_stop_aa", 56.90766, 24.18506, "a-"],
    ["eglaines_ieladole_tram_stop_aa", 56.90503, 24.1914, "a-"],
    #b-a
    ["eglaines_ieladole_tram_stop_ba", 56.90503, 24.1914, "-a"],
    ["malnavas_iela_tram_stop_ba", 56.90766, 24.18506, "-a"],
    ["rusonu_iela_tram_stop_ba", 56.91067, 24.17951, "-a"],
    ["prusu_iela_tram_stop_ba", 56.91422, 24.17554, "-a"],
    ["kengaraga_iela_tram_stop_ba", 56.91887, 24.17329, "-a"],
    ["dienvidu_tilts_tram_stop_ba", 56.92137, 24.17137, "-a"],
    ["krasta_masivs_tram_stop_ba", 56.92556, 24.16815, "-a"],
    ["atputas_centrs_lido_tram_stop_ba", 56.92708, 24.15909, "-a"],
    ["reznas_iela_tram_stop_ba", 56.93341, 24.15995, "-a"],
    ["latgales_parks_tram_stop_ba", 56.93599, 24.15587, "-a"],
    ["maza_kalna_iela_tram_stop_ba", 56.94232, 24.14533, "-a"],
    ["daugavpils_iela_tram_stop_ba", 56.93898, 24.14004, "-a"],
    ["katolu_iela_tram_stop_ba", 56.93958, 24.13549, "-a"],
    ["elijas_iela_tram_stop_ba", 56.93988, 24.12574, "-a"],
    ["jezusbaznicas_iela_tram_stop_ba", 56.94104, 24.1208, "-a"],
    ["spikeri_tram_stop_ba", 56.94234, 24.11619, "-a"],
    ["autoosta_tram_stop_ba", 56.94639, 24.11635, "-a"],
    ["nacionala_opera_tram_stop_ba", 56.94863, 24.11399, "-a"],
    ["nacionalais_teatris_tram_stop_ba", 56.95377, 24.10646, "-a"],
    ["ausekla_iela_tram_stop_ba", 56.95742, 24.10083, "-a"]
]
# Visi  maršruti (var pievienot vēlāk)
ROUTES = {
    "1": trol_3_stops + trol_5_stops,   # trolejbuss
    "2": bus_13_stops,    # autobuss
    "3": tram_11_stops + tram_7_stops  # tramvajs
}

allowed_sequences = [
    "1,3,",
    "1,5,",
    "2,13,",
    "3,11,",
    "3,7,",
]

invalidChars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

while True:
    fetch_data()

    print("Waiting for 5 seconds...")
    print("\n")
    time.sleep(5)


# 2 ir autobusi
# 1 trolejbusi
# 3 tramvaji

#24192407(garums WE),56983048 (platums NS)
#a-b (no centra)
#b-a (uz centru)
