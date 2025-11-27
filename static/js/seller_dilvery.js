const cities = {
  Lahore:     { lat: 31.5204, lng: 74.3587 },
  Karachi:    { lat: 24.8607, lng: 67.0011 },
  Islamabad:  { lat: 33.6844, lng: 73.0479 },
  Faisalabad: { lat: 31.4504, lng: 73.1350 },
  Multan:     { lat: 30.1575, lng: 71.5249 },
  Sahiwal:    { lat: 30.6680, lng: 73.1113 },
  Sialkot:    { lat: 32.4945, lng: 74.5229 },
  Gujranwala: { lat: 32.1877, lng: 74.1945 },
  Rawalpindi: { lat: 33.5651, lng: 73.0169 },
  Peshawar:   { lat: 34.0151, lng: 71.5249 }
};

let map, marker, circle;

function initMap() {
  map = L.map('map').setView([31.0, 70.0], 6);
  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '© CartoDB'
  }).addTo(map);
}

function updateAll() {
  const city = document.getElementById('baseCity').value;
  const radius = document.getElementById('radiusSlider').value;
  document.getElementById('radiusVal').textContent = radius;

  if (!city) {
    document.getElementById('cityTags').innerHTML = '<span class="text-gray-500 text-xs">Select city</span>';
    if (marker) map.removeLayer(marker);
    if (circle) map.removeLayer(circle);
    return;
  }

  const pos = cities[city];
  const latlng = [pos.lat, pos.lng];

  if (!marker) {
    marker = L.marker(latlng).addTo(map).bindPopup(city).openPopup();
  } else {
    marker.setLatLng(latlng);
  }

  if (!circle) {
    circle = L.circle(latlng, { radius: radius * 1000, color: '#1e40af', weight: 3, fillOpacity: 0.15 }).addTo(map);
  } else {
    circle.setLatLng(latlng).setRadius(radius * 1000);
  }

  map.setView(latlng, 8);

  // Covered cities
  const covered = Object.keys(cities).filter(c => {
    const d = map.distance(latlng, [cities[c].lat, cities[c].lng]) / 1000;
    return d <= radius;
  });

  const tags = document.getElementById('cityTags');
  tags.innerHTML = '';
  covered.forEach(c => {
    const span = document.createElement('span');
    span.className = 'city-tag';
    span.textContent = c;
    tags.appendChild(span);
  });
}

function saveSettings() {
  const city = document.getElementById('baseCity').value;
  const radius = document.getElementById('radiusSlider').value;
  if (!city) return alert("Select city first!");

  localStorage.setItem('deliveryCity', city);
  localStorage.setItem('deliveryRadius', radius);

  document.getElementById('savedStatus').classList.remove('hidden');
  setTimeout(() => document.getElementById('savedStatus').classList.add('hidden'), 2000);
}

// Events
document.getElementById('baseCity').addEventListener('change', updateAll);
document.getElementById('radiusSlider').addEventListener('input', updateAll);

// Load saved
window.onload = () => {
  initMap();
  const city = localStorage.getItem('deliveryCity');
  const radius = localStorage.getItem('deliveryRadius');
  if (city) {
    document.getElementById('baseCity').value = city;
    if (radius) document.getElementById('radiusSlider').value = radius;
    updateAll();
  }
};