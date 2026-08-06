const messages={
  ar:{brand:"المنصة الوطنية السورية للعناوين",pilot:"خريطة وطنية · إدارة محلية موحدة",admin:"الإدارة",national:"الجمهورية العربية السورية",headline:"العناوين والطرق<br>في خريطة واحدة.",intro:"ابحث، قرّب الخريطة واختر أي موقع. تصبح البيانات رسمية فقط بعد اعتماد البلدية.",searchLabel:"العنوان أو الشارع أو الرمز البريدي",search:"بحث",allSyria:"كل سوريا",maskanah:"مسكنة",results:"النتائج",dataStatus:"حالة البيانات",quality:"خريطة الأساس مفتوحة المصدر. أرقام المنازل الرسمية تُنشر فقط بعد التحقق.",mapReady:"الخريطة التفاعلية جاهزة",selectedPoint:"النقطة المختارة",hits:"نتيجة",none:"لا توجد نتائج رسمية.",systemOnline:"النظام متاح",mapTitle:"الخريطة الوطنية",layers:"طبقات الخريطة",layersHelp:"اختر المعلومات المرئية",roads:"طرق مسكنة",buildings:"مباني مسكنة",addresses:"العناوين الرسمية",numbers:"أرقام المنازل",official:"رسمي",draft:"قيد التحقق",pdf:"تنزيل ملف PDF",streetMap:"خريطة",satellite:"قمر صناعي",threeD:"ثلاثي الأبعاد",object:"الكائن",provisionalHeight:"ارتفاع تقريبي"},
  en:{brand:"Syria National Address Platform",pilot:"National map · unified local administration",admin:"Administration",national:"Syrian Arab Republic",headline:"Addresses and roads<br>in one map.",intro:"Search, zoom and select any location. Data becomes official only after municipal approval.",searchLabel:"Address, street or postal code",search:"Search",allSyria:"All Syria",maskanah:"Maskanah",results:"Results",dataStatus:"Data status",quality:"The basemap is open-source. Official house numbers appear only after verification.",mapReady:"Interactive map ready",selectedPoint:"Selected point",hits:"results",none:"No official result.",systemOnline:"System available",mapTitle:"National map",layers:"Map layers",layersHelp:"Choose visible information",roads:"Maskanah roads",buildings:"Maskanah buildings",addresses:"Official addresses",numbers:"House numbers",official:"Official",draft:"Verification pending",pdf:"Download PDF dossier",streetMap:"Map",satellite:"Satellite",threeD:"3D",object:"Object",provisionalHeight:"Provisional height"},
  de:{brand:"Nationale Adressplattform Syriens",pilot:"Landeskarte · einheitliche Kommunalverwaltung",admin:"Verwaltung",national:"Syrische Arabische Republik",headline:"Adressen und Straßen<br>auf einer Karte.",intro:"Suchen, zoomen und jeden Ort auswählen. Daten werden erst nach kommunaler Freigabe amtlich.",searchLabel:"Adresse, Straße oder Postleitzahl",search:"Suchen",allSyria:"Ganz Syrien",maskanah:"Maskanah",results:"Ergebnisse",dataStatus:"Datenstatus",quality:"Die Basiskarte ist Open Source. Amtliche Hausnummern erscheinen erst nach Prüfung.",mapReady:"Interaktive Karte bereit",selectedPoint:"Ausgewählter Punkt",hits:"Treffer",none:"Kein amtliches Ergebnis.",systemOnline:"System verfügbar",mapTitle:"Nationale Karte",layers:"Kartenebenen",layersHelp:"Sichtbare Informationen auswählen",roads:"Straßen Maskanah",buildings:"Gebäude Maskanah",addresses:"Amtliche Adressen",numbers:"Hausnummern",official:"Amtlich",draft:"Prüfung ausstehend",pdf:"PDF-Objektakte herunterladen",streetMap:"Karte",satellite:"Satellit",threeD:"3D",object:"Objekt",provisionalHeight:"Vorläufige Höhe"}
};
Object.assign(messages.ar,{maskanah:"الزبداني",roads:"طرق الزبداني",buildings:"مباني الزبداني"});
Object.assign(messages.en,{maskanah:"Al-Zabadani",roads:"Al-Zabadani roads",buildings:"Al-Zabadani buildings"});
Object.assign(messages.de,{maskanah:"Al-Zabadani",roads:"Straßen Al-Zabadani",buildings:"Gebäude Al-Zabadani"});
Object.assign(messages.ar,{cadastral:"السجل"});
Object.assign(messages.en,{cadastral:"Register"});
Object.assign(messages.de,{cadastral:"Kataster"});
const $=selector=>document.querySelector(selector);
const esc=value=>String(value??"").replace(/[&<>"']/g,char=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));
let lang=localStorage.getItem("sna-lang")||"ar";
let is3d=false;
let basemapMode="street";
let loaded={roads:null,buildings:null,addresses:null,boundary:null};
function syriaOutsideMask(boundary){
  const feature=boundary?.features?.[0]||boundary;
  const geometry=feature?.geometry;
  if(!geometry||geometry.type!=="Polygon"||!geometry.coordinates?.[0])return {type:"FeatureCollection",features:[]};
  const close=ring=>{
    const result=ring.map(point=>[Number(point[0]),Number(point[1])]);
    if(result.length&&String(result[0])!==String(result[result.length-1]))result.push([...result[0]]);
    return result;
  };
  const signedArea=ring=>ring.slice(0,-1).reduce((sum,point,index)=>{
    const next=ring[index+1];
    return sum+(point[0]*next[1]-next[0]*point[1]);
  },0)/2;
  const orient=(ring,counterClockwise)=>{
    const closed=close(ring);
    return (signedArea(closed)>0)===counterClockwise?closed:closed.slice().reverse();
  };
  const world=orient([[-179.9,-84],[179.9,-84],[179.9,84],[-179.9,84],[-179.9,-84]],true);
  const syriaHole=orient(geometry.coordinates[0],false);
  return {type:"FeatureCollection",features:[{type:"Feature",properties:{purpose:"outside-syria-mask"},geometry:{type:"Polygon",coordinates:[world,syriaHole]}}]};
}
let numberMarkers=[];

function applyLanguage(){
  document.documentElement.lang=lang;
  document.documentElement.dir=lang==="ar"?"rtl":"ltr";
  $("#language").value=lang;
  document.querySelectorAll("[data-i18n]").forEach(element=>{
    const value=messages[lang][element.dataset.i18n];
    if(value!==undefined)element.innerHTML=value;
  });
}

const style={
  version:8,
  glyphs:"https://demotiles.maplibre.org/font/{fontstack}/{range}.pbf",
  sources:{
    streets:{type:"raster",tiles:["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],tileSize:256,attribution:"© OpenStreetMap contributors"},
    satellite:{type:"raster",tiles:["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"],tileSize:256,maxzoom:17,attribution:"Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community"}
  },
  layers:[
    {id:"street-basemap",type:"raster",source:"streets"},
    {id:"satellite-basemap",type:"raster",source:"satellite",layout:{visibility:"none"}},
    {id:"cadastral-background",type:"background",layout:{visibility:"none"},paint:{"background-color":"#f7f1f3"}}
  ]
};

const map=new maplibregl.Map({
  container:"national-map",
  style,
  center:[38.4,35.0],
  zoom:5.7,
  pitch:0,
  bearing:0,
  antialias:true,
  attributionControl:true,
  maxPitch:75
});
map.addControl(new maplibregl.NavigationControl({visualizePitch:true}),"bottom-left");
map.addControl(new maplibregl.ScaleControl({unit:"metric"}),"bottom-left");

async function loadLayers(){
  [loaded.roads,loaded.buildings,loaded.addresses,loaded.boundary]=await Promise.all([
    fetch("/api/v1/map/zabadani/roads").then(response=>response.json()),
    fetch("/api/v1/map/zabadani/buildings").then(response=>response.json()),
    fetch("/api/v1/addresses?q=").then(response=>response.json()),
    fetch("/api/v1/map/syria/boundary").then(response=>response.json())
  ]);
  map.addSource("maskanah-roads",{type:"geojson",data:loaded.roads});
  map.addSource("maskanah-buildings",{type:"geojson",data:loaded.buildings});
  map.addSource("official-addresses",{type:"geojson",data:loaded.addresses});
  map.addSource("syria-boundary",{type:"geojson",data:loaded.boundary});
  map.addSource("syria-outside-mask",{type:"geojson",data:syriaOutsideMask(loaded.boundary)});
  map.addLayer({id:"syria-outside-white",type:"fill",source:"syria-outside-mask",paint:{"fill-color":"#ffffff","fill-opacity":1,"fill-antialias":false}});
  map.addLayer({id:"syria-territory",type:"fill",source:"syria-boundary",paint:{"fill-color":"#0b6b4c","fill-opacity":["interpolate",["linear"],["zoom"],4,0.12,8,0.035,10,0]}});
  map.addLayer({id:"maskanah-buildings-flat",type:"fill",source:"maskanah-buildings",minzoom:11,paint:{"fill-color":"#d9b76e","fill-outline-color":"#675937","fill-opacity":0.75}});
  map.addLayer({id:"maskanah-buildings-3d",type:"fill-extrusion",source:"maskanah-buildings",minzoom:12,layout:{visibility:"none"},paint:{"fill-extrusion-color":["interpolate",["linear"],["zoom"],12,"#c8b083",17,"#e3c987"],"fill-extrusion-height":["coalesce",["to-number",["get","height"]],["*",["to-number",["get","building_levels"]],3],9],"fill-extrusion-base":0,"fill-extrusion-opacity":0.92}});
  map.addLayer({id:"cadastral-road-casing",type:"line",source:"maskanah-roads",minzoom:12,layout:{visibility:"none"},paint:{"line-color":"#71777a","line-width":["interpolate",["linear"],["zoom"],12,4,17,13],"line-opacity":1}});
  map.addLayer({id:"maskanah-roads",type:"line",source:"maskanah-roads",minzoom:10,paint:{"line-color":"#0b6b4c","line-width":["interpolate",["linear"],["zoom"],10,1,17,5],"line-opacity":0.88}});
  map.addLayer({id:"cadastral-road-labels",type:"symbol",source:"maskanah-roads",minzoom:13,layout:{visibility:"none","symbol-placement":"line","text-field":["coalesce",["get","name_ar"],["get","name_en"],""],"text-font":["Open Sans Regular"],"text-size":["interpolate",["linear"],["zoom"],13,10,17,14],"text-allow-overlap":false,"text-padding":6},paint:{"text-color":"#20272a","text-halo-color":"#ffffff","text-halo-width":2}});
  map.addLayer({id:"official-addresses",type:"circle",source:"official-addresses",paint:{"circle-radius":6,"circle-color":"#0b6b4c","circle-stroke-color":"#fff","circle-stroke-width":2}});
  map.addLayer({id:"syria-national-border-glow",type:"line",source:"syria-boundary",paint:{"line-color":"#ffffff","line-width":["interpolate",["linear"],["zoom"],4,7,9,5,14,3],"line-opacity":1}});
  map.addLayer({id:"syria-national-border",type:"line",source:"syria-boundary",paint:{"line-color":"#0b6b4c","line-width":["interpolate",["linear"],["zoom"],4,3.8,9,2.8,14,1.8],"line-opacity":1}});
  numberMarkers=loaded.addresses.features.filter(feature=>feature.properties.house_number).map(feature=>{
    const element=document.createElement("div");
    element.className="house-number-marker";
    element.textContent=feature.properties.house_number;
    element.style.display="none";
    return new maplibregl.Marker({element}).setLngLat(feature.geometry.coordinates).addTo(map);
  });
  map.on("click","maskanah-buildings-3d",showBuilding);
  map.on("click","maskanah-buildings-flat",showBuilding);
  map.on("mouseenter","maskanah-buildings-3d",()=>map.getCanvas().style.cursor="pointer");
  map.on("mouseleave","maskanah-buildings-3d",()=>map.getCanvas().style.cursor="");
}

function showBuilding(event){
  const feature=event.features[0];
  const properties=feature.properties||{};
  new maplibregl.Popup().setLngLat(event.lngLat).setHTML(`<strong>${esc(messages[lang].object)}</strong><br>${esc(properties.technical_code||feature.id)}<br><small>${esc(messages[lang].provisionalHeight)}: 9 m</small>`).addTo(map);
}

map.on("load",loadLayers);
map.on("click",event=>{
  $("#coordinate-value").textContent=`${event.lngLat.lat.toFixed(6)}, ${event.lngLat.lng.toFixed(6)}`;
  $("#coordinate-card").classList.remove("hidden");
});
map.on("moveend",()=>{
  const center=map.getCenter();
  $("#view-location").textContent=`${center.lat.toFixed(3)}, ${center.lng.toFixed(3)} · z${map.getZoom().toFixed(1)}`;
});

function setBasemap(mode){
  basemapMode=mode;
  map.setLayoutProperty("street-basemap","visibility",mode==="street"?"visible":"none");
  map.setLayoutProperty("satellite-basemap","visibility",mode==="satellite"?"visible":"none");
  map.setLayoutProperty("cadastral-background","visibility",mode==="cadastral"?"visible":"none");
  if(map.getLayer("cadastral-road-casing"))map.setLayoutProperty("cadastral-road-casing","visibility",mode==="cadastral"&&$("#layer-roads").checked?"visible":"none");
  if(map.getLayer("cadastral-road-labels"))map.setLayoutProperty("cadastral-road-labels","visibility",mode==="cadastral"&&$("#layer-roads").checked?"visible":"none");
  if(map.getLayer("maskanah-buildings-flat")){
    map.setPaintProperty("maskanah-buildings-flat","fill-color",mode==="cadastral"?"#aeb3b5":"#d9b76e");
    map.setPaintProperty("maskanah-buildings-flat","fill-outline-color",mode==="cadastral"?"#555d61":"#675937");
    map.setPaintProperty("maskanah-buildings-flat","fill-opacity",mode==="cadastral"?0.92:0.75);
  }
  if(map.getLayer("maskanah-roads")){
    map.setPaintProperty("maskanah-roads","line-color",mode==="cadastral"?"#ffffff":"#0b6b4c");
    map.setPaintProperty("maskanah-roads","line-width",mode==="cadastral"?["interpolate",["linear"],["zoom"],12,2.8,17,11]:["interpolate",["linear"],["zoom"],10,1,17,5]);
    map.setPaintProperty("maskanah-roads","line-opacity",mode==="cadastral"?1:0.88);
  }
  if(mode==="cadastral"&&is3d)toggle3d();
  numberMarkers.forEach(marker=>marker.getElement().style.display=mode==="cadastral"||$("#layer-numbers").checked?"block":"none");
  $("#cadastral-view").classList.toggle("active",mode==="cadastral");
  $("#street-view").classList.toggle("active",mode==="street");
  $("#satellite-view").classList.toggle("active",mode==="satellite");
}

function toggle3d(){
  is3d=!is3d;
  $("#toggle-3d").classList.toggle("active",is3d);
  if(map.getLayer("maskanah-buildings-3d")){
    map.setLayoutProperty("maskanah-buildings-3d","visibility",is3d&&$("#layer-buildings").checked?"visible":"none");
    map.setLayoutProperty("maskanah-buildings-flat","visibility",!is3d&&$("#layer-buildings").checked?"visible":"none");
  }
  map.easeTo({pitch:is3d?58:0,bearing:is3d?18:0,duration:900});
}

function focusItem(item){
  if(item.longitude!=null&&item.latitude!=null){
    map.flyTo({center:[+item.longitude,+item.latitude],zoom:item.object_type==="PLACE"?12:17,pitch:is3d?58:0,duration:1000});
  }
}

async function search(){
  const m=messages[lang],query=$("#q").value.trim();
  let items;
  if(!query){
    const data=await fetch("/api/v1/addresses?q=").then(response=>response.json());
    items=data.features.map(feature=>({object_type:"ADDRESS",id:feature.properties.id,technical_code:feature.properties.official_code,label_ar:feature.properties.name_ar,label_en:feature.properties.name_en,longitude:feature.geometry.coordinates[0],latitude:feature.geometry.coordinates[1],postal_code:feature.properties.postal_code,quality_level:feature.properties.quality_level,official_status:feature.properties.official_status}));
  }else{
    items=(await fetch("/api/v1/catalog/search?q="+encodeURIComponent(query)).then(response=>response.json())).items;
  }
  $("#count").textContent=items.length+" "+m.hits;
  $("#results").innerHTML=items.slice(0,80).map((item,index)=>`<article class="result" data-i="${index}"><div class="request-top"><strong dir="rtl">${esc(item.label_ar)}</strong><b>${esc(item.object_type)}</b></div><span>${esc(item.label_en||item.technical_code)}</span><div class="result-footer"><small class="badge">${esc(item.official_status)} · Q${esc(item.quality_level)}</small><a class="pdf-link" href="/api/v1/pdf/${encodeURIComponent(item.object_type)}/${encodeURIComponent(item.id)}" download>${esc(m.pdf)}</a></div></article>`).join("")||`<p class="muted">${m.none}</p>`;
  document.querySelectorAll(".result").forEach(element=>element.onclick=()=>focusItem(items[+element.dataset.i]));
  document.querySelectorAll(".pdf-link").forEach(element=>element.onclick=event=>event.stopPropagation());
}

$("#language").onchange=event=>{lang=event.target.value;localStorage.setItem("sna-lang",lang);applyLanguage()};
$("#search").onclick=search;
$("#q").onkeydown=event=>{if(event.key==="Enter")search()};
$("#show-syria").onclick=()=>{map.flyTo({center:[38.4,35],zoom:5.7,pitch:0,bearing:0});$("#show-syria").classList.add("active");$("#show-maskanah").classList.remove("active")};
$("#show-maskanah").onclick=()=>{map.flyTo({center:[36.1002,33.7244],zoom:15.3,pitch:is3d?58:0,bearing:is3d?18:0});$("#show-maskanah").classList.add("active");$("#show-syria").classList.remove("active")};
$("#fit-country").onclick=()=>map.fitBounds([[35.6,32.2],[42.4,37.4]],{padding:45,pitch:0,bearing:0});
$("#close-coordinate").onclick=event=>{event.stopPropagation();$("#coordinate-card").classList.add("hidden")};
$("#street-view").onclick=()=>setBasemap("street");
$("#satellite-view").onclick=()=>setBasemap("satellite");
$("#cadastral-view").onclick=()=>setBasemap("cadastral");
$("#toggle-3d").onclick=toggle3d;
$("#layer-roads").onchange=event=>{if(map.getLayer("maskanah-roads")){map.setLayoutProperty("maskanah-roads","visibility",event.target.checked?"visible":"none");map.setLayoutProperty("cadastral-road-casing","visibility",event.target.checked&&basemapMode==="cadastral"?"visible":"none");map.setLayoutProperty("cadastral-road-labels","visibility",event.target.checked&&basemapMode==="cadastral"?"visible":"none")}};
$("#layer-buildings").onchange=event=>{if(map.getLayer("maskanah-buildings-flat")){map.setLayoutProperty("maskanah-buildings-flat","visibility",event.target.checked&&!is3d?"visible":"none");map.setLayoutProperty("maskanah-buildings-3d","visibility",event.target.checked&&is3d?"visible":"none")}};
$("#layer-addresses").onchange=event=>map.getLayer("official-addresses")&&map.setLayoutProperty("official-addresses","visibility",event.target.checked?"visible":"none");
$("#layer-numbers").onchange=event=>numberMarkers.forEach(marker=>marker.getElement().style.display=event.target.checked||basemapMode==="cadastral"?"block":"none");
applyLanguage();
search();
