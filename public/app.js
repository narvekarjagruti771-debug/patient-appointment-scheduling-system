// ====================================================================
// MediFlow Client Side Logic
// Connects separate Patient, Doctor, and Developer Portals to Server APIs
// ====================================================================

const API_BASE = '/api';

// Global application state
let patients = [];
let doctors = [];
let patientAppointments = [];
let doctorAppointments = [];
let currentPatientId = null;
let currentDoctorId = null;

// Initialize app on page load
window.addEventListener('DOMContentLoaded', () => {
  checkDBConnection();
  
  // Set default report date and date restriction inputs to today
  const today = new Date().toISOString().split('T')[0];
  document.getElementById('p-appointment-date').min = today;
  document.getElementById('doctor-report-date').value = today;
});

// Check DB status on startup
async function checkDBConnection() {
  try {
    const res = await fetch(`${API_BASE}/doctors`);
    if (res.ok) {
      setDBStatus(true);
    } else {
      setDBStatus(false);
    }
  } catch (err) {
    console.error('Failed to connect to backend/DB:', err);
    setDBStatus(false);
    showAlert('Unable to connect to MySQL database! Please make sure XAMPP MySQL is started.', 'error');
  }
}

// ====================================================================
// PORTAL HUB NAVIGATION & INITIAL DATA RETRIEVAL
// ====================================================================
async function enterPortal(role) {
  // Hide landing screen and all portal containers
  document.getElementById('portal-landing').classList.remove('active-screen');
  document.querySelectorAll('.portal-screen').forEach(el => el.classList.remove('active-screen'));
  
  if (role === 'patient') {
    document.getElementById('portal-patient').classList.add('active-screen');
    await loadPatientPortalData();
    switchPatientTab('p-book');
  } else if (role === 'doctor') {
    document.getElementById('portal-doctor').classList.add('active-screen');
    await loadDoctorPortalData();
    switchDoctorTab('d-queue');
  } else if (role === 'developer') {
    document.getElementById('portal-developer').classList.add('active-screen');
    await loadDeveloperPortalData();
    switchDevTab('dev-stats');
  }
}

function goHome() {
  // Reset active state references
  currentPatientId = null;
  currentDoctorId = null;
  
  // Reset profiles UI
  document.getElementById('patient-selector').value = '';
  document.getElementById('patient-profile-badge').classList.add('hidden');
  document.getElementById('patient-booking-form-wrapper').classList.add('hidden');
  document.getElementById('patient-history-wrapper').classList.add('hidden');
  document.getElementById('patient-no-selection-view').classList.remove('hidden');
  
  document.getElementById('doctor-selector').value = '';
  document.getElementById('doctor-profile-badge').classList.add('hidden');
  document.getElementById('doctor-queue-wrapper').classList.add('hidden');
  document.getElementById('doctor-reports-wrapper').classList.add('hidden');
  document.getElementById('doctor-no-selection-view').classList.remove('hidden');

  // Hide portal containers, show landing
  document.querySelectorAll('.portal-screen').forEach(el => el.classList.remove('active-screen'));
  document.getElementById('portal-landing').classList.add('active-screen');
  
  checkDBConnection();
}

// ====================================================================
// PATIENT PORTAL INTERACTION
// ====================================================================
async function loadPatientPortalData() {
  try {
    // Fetch patients to fill the active patient dropdown
    const patsRes = await fetch(`${API_BASE}/patients`);
    patients = await patsRes.json();
    populatePatientSelectors(patients);

    // Fetch doctors to fill the booking dropdown
    const docsRes = await fetch(`${API_BASE}/doctors`);
    doctors = await docsRes.json();
    populateDoctorBookingDropdown(doctors);
  } catch (err) {
    console.error('Failed to load Patient portal setup data:', err);
    showAlert('Database error. Unable to load patient list.', 'error');
  }
}

function populatePatientSelectors(list) {
  const selector = document.getElementById('patient-selector');
  selector.innerHTML = '<option value="" disabled selected>-- Select Profile --</option>';
  list.forEach(p => {
    const opt = document.createElement('option');
    opt.value = p.patient_id;
    opt.textContent = `${p.name} (${p.phone})`;
    selector.appendChild(opt);
  });
}

function populateDoctorBookingDropdown(list) {
  const select = document.getElementById('p-select-doctor');
  select.innerHTML = '<option value="" disabled selected>-- Select Doctor --</option>';
  list.forEach(d => {
    const opt = document.createElement('option');
    opt.value = d.doctor_id;
    opt.textContent = `Dr. ${d.name} (${d.specialization})`;
    select.appendChild(opt);
  });
}

// Triggered when patient selects their identity
async function onPatientSelect() {
  const select = document.getElementById('patient-selector');
  currentPatientId = select.value;
  
  if (!currentPatientId) return;

  const activePatientObj = patients.find(p => p.patient_id == currentPatientId);
  if (activePatientObj) {
    // Show patient UI panels
    document.getElementById('current-patient-name').textContent = activePatientObj.name;
    document.getElementById('patient-profile-badge').classList.remove('hidden');
    document.getElementById('patient-booking-form-wrapper').classList.remove('hidden');
    document.getElementById('patient-history-wrapper').classList.remove('hidden');
    document.getElementById('patient-no-selection-view').classList.add('hidden');
    
    // Fetch patient appointments history using the filtered view endpoint
    fetchPatientAppointments(currentPatientId);
  }
}

async function fetchPatientAppointments(patientId) {
  try {
    const res = await fetch(`${API_BASE}/patients/${patientId}/appointments`);
    patientAppointments = await res.json();
    renderPatientHistory(patientAppointments);
  } catch (err) {
    console.error(err);
    showAlert('Error fetching patient appointments.', 'error');
  }
}

function renderPatientHistory(appts) {
  const tbody = document.getElementById('patient-history-table-body');
  tbody.innerHTML = '';
  
  if (appts.length === 0) {
    tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">No appointments found. Book one to start!</td></tr>';
    return;
  }

  appts.forEach(app => {
    const dateObj = new Date(app.appointment_date);
    const dateStr = dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    const timeStr = app.appointment_time.slice(0, 5);

    tbody.innerHTML += `
      <tr>
        <td><strong>#${app.appointment_id}</strong></td>
        <td>Dr. ${app.doctor_name}</td>
        <td><span class="badge" style="background: rgba(255,255,255,0.06); font-size:10px;">${app.doctor_specialization}</span></td>
        <td>${dateStr}</td>
        <td><i class="fa-regular fa-clock"></i> ${timeStr}</td>
        <td><span class="text-secondary">${app.reason}</span></td>
        <td><span class="status-pill status-${app.status.toLowerCase()}">${app.status}</span></td>
      </tr>
    `;
  });
}

function switchPatientTab(tabId) {
  // Navigation tabs styling toggle
  document.querySelectorAll('.patient-sidebar .nav-btn').forEach(btn => btn.classList.remove('active'));
  document.getElementById(`btn-${tabId}`).classList.add('active');
  
  // Tab panels toggle
  document.querySelectorAll('.patient-tab-content').forEach(content => content.classList.remove('active'));
  document.getElementById(`tab-${tabId}`).classList.add('active');

  const title = document.getElementById('patient-page-title');
  const subtitle = document.getElementById('patient-page-subtitle');
  
  if (tabId === 'p-book') {
    title.textContent = 'Book an Appointment';
    subtitle.textContent = 'Schedule a consultation with our specialist doctors';
  } else if (tabId === 'p-history') {
    title.textContent = 'Booking History';
    subtitle.textContent = 'Manage and review your consultation appointments';
    if (currentPatientId) fetchPatientAppointments(currentPatientId);
  } else if (tabId === 'p-viewinfo') {
    title.textContent = 'Virtual Table View';
    subtitle.textContent = 'Learn how SQL View upcoming_appointments_view queries your personal bookings';
  }
}

// Modal handling
function showPatientRegModal() {
  document.getElementById('patient-reg-modal').classList.remove('hidden');
}

function closePatientRegModal() {
  document.getElementById('patient-reg-modal').classList.add('hidden');
  document.getElementById('patient-reg-form').reset();
}

// Handle Patient Registration form (POST /api/patients)
async function handlePatientRegister(event) {
  event.preventDefault();
  const name = document.getElementById('reg-name').value;
  const email = document.getElementById('reg-email').value;
  const phone = document.getElementById('reg-phone').value;
  const dob = document.getElementById('reg-dob').value;
  const gender = document.getElementById('reg-gender').value;

  try {
    const res = await fetch(`${API_BASE}/patients`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, phone, dob, gender })
    });
    const data = await res.json();
    
    if (res.ok) {
      showAlert('Success! Patient profile registered.', 'success');
      closePatientRegModal();
      
      // Reload Patient profiles
      const patsRes = await fetch(`${API_BASE}/patients`);
      patients = await patsRes.json();
      populatePatientSelectors(patients);
      
      // Auto-select the newly registered patient
      document.getElementById('patient-selector').value = data.patient_id;
      onPatientSelect();
    } else {
      showAlert(`Registration failed: ${data.error}`, 'error');
    }
  } catch (err) {
    console.error(err);
    showAlert('Server connection error. Registration failed.', 'error');
  }
}

// Book Appointment from Patient Portal (POST /api/appointments)
// Fires "after_appointment_insert" trigger on DB
async function handlePatientBook(event) {
  event.preventDefault();
  if (!currentPatientId) {
    showAlert('Please select your Patient Profile first.', 'error');
    return;
  }

  const submitBtn = document.getElementById('btn-patient-submit');
  submitBtn.disabled = true;
  submitBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Processing...';

  const appointmentData = {
    patient_id: parseInt(currentPatientId),
    doctor_id: parseInt(document.getElementById('p-select-doctor').value),
    appointment_date: document.getElementById('p-appointment-date').value,
    appointment_time: document.getElementById('p-appointment-time').value,
    reason: document.getElementById('p-appointment-reason').value
  };

  try {
    const res = await fetch(`${API_BASE}/appointments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(appointmentData)
    });
    const data = await res.json();
    
    if (res.ok) {
      showAlert('Success! Appointment booked. Database Trigger automatically logged this activity.', 'success');
      document.getElementById('patient-appointment-form').reset();
      
      // Refresh appointment list history tab
      fetchPatientAppointments(currentPatientId);
    } else {
      showAlert(`Error: ${data.error}`, 'error');
    }
  } catch (err) {
    console.error(err);
    showAlert('Server connection error. Failed to book appointment.', 'error');
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = '<i class="fa-solid fa-circle-check"></i> Book Consultation';
  }
}


// ====================================================================
// DOCTOR PORTAL INTERACTION
// ====================================================================
async function loadDoctorPortalData() {
  try {
    const docsRes = await fetch(`${API_BASE}/doctors`);
    doctors = await docsRes.json();
    populateDoctorSelectors(doctors);
  } catch (err) {
    console.error(err);
    showAlert('Error fetching doctor list.', 'error');
  }
}

function populateDoctorSelectors(list) {
  const selector = document.getElementById('doctor-selector');
  selector.innerHTML = '<option value="" disabled selected>-- Select Doctor --</option>';
  list.forEach(d => {
    const opt = document.createElement('option');
    opt.value = d.doctor_id;
    opt.textContent = `Dr. ${d.name} (${d.specialization})`;
    selector.appendChild(opt);
  });
}

function onDoctorSelect() {
  const selector = document.getElementById('doctor-selector');
  currentDoctorId = selector.value;
  if (!currentDoctorId) return;

  const activeDocObj = doctors.find(d => d.doctor_id == currentDoctorId);
  if (activeDocObj) {
    document.getElementById('current-doctor-name').textContent = `Dr. ${activeDocObj.name}`;
    document.getElementById('doctor-profile-badge').classList.remove('hidden');
    document.getElementById('doctor-queue-wrapper').classList.remove('hidden');
    document.getElementById('doctor-reports-wrapper').classList.remove('hidden');
    document.getElementById('doctor-no-selection-view').classList.add('hidden');

    fetchDoctorAppointments(currentDoctorId);
  }
}

async function fetchDoctorAppointments(doctorId) {
  try {
    const res = await fetch(`${API_BASE}/doctors/${doctorId}/appointments`);
    doctorAppointments = await res.json();
    renderDoctorQueue(doctorAppointments);
  } catch (err) {
    console.error(err);
    showAlert('Error fetching doctor queue.', 'error');
  }
}

function renderDoctorQueue(list) {
  const tbody = document.getElementById('doctor-queue-table-body');
  tbody.innerHTML = '';
  
  if (list.length === 0) {
    tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">No appointments found in your queue.</td></tr>';
    return;
  }

  list.forEach(app => {
    const dateObj = new Date(app.appointment_date);
    const dateStr = dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    const timeStr = app.appointment_time.slice(0, 5);

    let actionButtons = '';
    if (app.status === 'Scheduled') {
      actionButtons = `
        <button class="btn-sm-action btn-complete" title="Mark Complete" onclick="changeAppointmentStatus(${app.appointment_id}, 'Completed')">
          <i class="fa-solid fa-check"></i> Complete
        </button>
        <button class="btn-sm-action btn-cancel" title="Cancel Appointment" onclick="changeAppointmentStatus(${app.appointment_id}, 'Cancelled')">
          <i class="fa-solid fa-xmark"></i> Cancel
        </button>
      `;
    } else {
      actionButtons = `<span class="text-muted" style="font-size:11px;">Completed</span>`;
    }

    tbody.innerHTML += `
      <tr>
        <td><strong>#${app.appointment_id}</strong></td>
        <td>${app.patient_name}</td>
        <td><span class="text-secondary" style="font-size:12px;">${app.patient_phone}</span></td>
        <td>${dateStr}</td>
        <td><i class="fa-regular fa-clock"></i> ${timeStr}</td>
        <td><span class="text-secondary">${app.reason}</span></td>
        <td><span class="status-pill status-${app.status.toLowerCase()}">${app.status}</span></td>
        <td>${actionButtons}</td>
      </tr>
    `;
  });
}

function switchDoctorTab(tabId) {
  document.querySelectorAll('.doctor-sidebar .nav-btn').forEach(btn => btn.classList.remove('active'));
  document.getElementById(`btn-${tabId}`).classList.add('active');
  
  document.querySelectorAll('.doctor-tab-content').forEach(content => content.classList.remove('active'));
  document.getElementById(`tab-${tabId}`).classList.add('active');

  const title = document.getElementById('doctor-page-title');
  const subtitle = document.getElementById('doctor-page-subtitle');
  
  if (tabId === 'd-queue') {
    title.textContent = 'Patient Schedule Queue';
    subtitle.textContent = 'Review your queue of patient scheduled sessions';
    if (currentDoctorId) fetchDoctorAppointments(currentDoctorId);
  } else if (tabId === 'd-cursor') {
    title.textContent = 'Daily Agenda Cursor Reports';
    subtitle.textContent = 'Loop through appointments tables with stored procedure cursors';
  }
}

function filterDoctorQueue() {
  const filterVal = document.getElementById('doctor-queue-filter-status').value;
  
  const filtered = doctorAppointments.filter(app => {
    return filterVal === 'ALL' || app.status === filterVal;
  });
  renderDoctorQueue(filtered);
}

// Update status of appointment (PUT /api/appointments/:id/status)
// Automatically triggers `after_appointment_update` on DB
async function changeAppointmentStatus(apptId, newStatus) {
  try {
    const res = await fetch(`${API_BASE}/appointments/${apptId}/status`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    });
    const data = await res.json();
    
    if (res.ok) {
      showAlert(`Appointment #${apptId} status updated to ${newStatus}. Trigger logged it!`, 'success');
      // Refresh doctor queue
      fetchDoctorAppointments(currentDoctorId);
    } else {
      showAlert(`Failed to update appointment: ${data.error}`, 'error');
    }
  } catch (err) {
    console.error(err);
    showAlert('Server connection error.', 'error');
  }
}

// Run SQL Stored Procedure that uses cursor (POST /api/reports/generate)
async function handleDoctorGenerateReport(event) {
  event.preventDefault();
  const generateBtn = document.getElementById('btn-doctor-generate-report');
  generateBtn.disabled = true;
  generateBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Executing Procedure...';

  const dateVal = document.getElementById('doctor-report-date').value;

  try {
    const res = await fetch(`${API_BASE}/reports/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date: dateVal })
    });
    const data = await res.json();
    
    if (res.ok) {
      showAlert('MySQL Cursor stored procedure executed & report saved!', 'success');
      
      const outputBox = document.getElementById('doctor-report-output-text');
      outputBox.textContent = data.report_summary;
      
      const badge = document.getElementById('doctor-report-timestamp-badge');
      badge.textContent = `Generated: ${new Date(data.generated_at).toLocaleString()}`;
    } else {
      showAlert(`SP Error: ${data.error}`, 'error');
    }
  } catch (err) {
    console.error(err);
    showAlert('Server connection error. Failed to run SP.', 'error');
  } finally {
    generateBtn.disabled = false;
    generateBtn.innerHTML = '<i class="fa-solid fa-gears"></i> Run SQL Cursor SP';
  }
}


// ====================================================================
// DBMS DEVELOPER LAB INTERACTION
// ====================================================================
async function loadDeveloperPortalData() {
  // Fetch stats and trigger logs
  fetchDeveloperStats();
  fetchDeveloperRawAppointments();
  fetchDeveloperLogs();
  fetchDeveloperReports();
}

async function fetchDeveloperStats() {
  try {
    const patsRes = await fetch(`${API_BASE}/patients`);
    const pats = await patsRes.json();
    document.getElementById('dev-stat-patients').textContent = pats.length;

    const docsRes = await fetch(`${API_BASE}/doctors`);
    const docs = await docsRes.json();
    document.getElementById('dev-stat-doctors').textContent = docs.length;

    const apptsRes = await fetch(`${API_BASE}/appointments`);
    const appts = await apptsRes.json();
    document.getElementById('dev-stat-appointments').textContent = appts.length;
  } catch (err) {
    console.error(err);
  }
}

async function fetchDeveloperRawAppointments() {
  try {
    const res = await fetch(`${API_BASE}/appointments`);
    const list = await res.json();
    const tbody = document.getElementById('dev-raw-table-body');
    tbody.innerHTML = '';
    
    if (list.length === 0) {
      tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">No appointments inside the view.</td></tr>';
      return;
    }

    list.forEach(app => {
      const dateObj = new Date(app.appointment_date);
      const dateStr = dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
      const timeStr = app.appointment_time.slice(0, 5);

      tbody.innerHTML += `
        <tr>
          <td><strong>#${app.appointment_id}</strong></td>
          <td>${app.patient_name}</td>
          <td><span class="text-secondary">${app.patient_phone}</span></td>
          <td>Dr. ${app.doctor_name}</td>
          <td><span class="badge" style="background: rgba(255,255,255,0.06); font-size:10px;">${app.doctor_specialization}</span></td>
          <td>${dateStr} @ ${timeStr}</td>
          <td><span class="text-secondary">${app.reason}</span></td>
          <td><span class="status-pill status-${app.status.toLowerCase()}">${app.status}</span></td>
        </tr>
      `;
    });
  } catch (err) {
    console.error(err);
  }
}

async function fetchDeveloperLogs() {
  try {
    const res = await fetch(`${API_BASE}/logs`);
    const logs = await res.json();
    const tbody = document.getElementById('dev-logs-table-body');
    tbody.innerHTML = '';

    if (logs.length === 0) {
      tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">No activities have fired database triggers yet.</td></tr>';
      return;
    }

    logs.forEach(log => {
      const timeStr = new Date(log.log_timestamp).toLocaleString();
      tbody.innerHTML += `
        <tr>
          <td><code class="code-sm">#L-${log.log_id}</code></td>
          <td><strong>#${log.appointment_id}</strong></td>
          <td><span class="log-action-pill action-${log.action_type.toLowerCase()}">${log.action_type}</span></td>
          <td><span class="text-muted">${log.old_status || 'NULL'}</span></td>
          <td><span class="status-pill status-${log.new_status.toLowerCase()}">${log.new_status}</span></td>
          <td><span class="text-secondary" style="font-size:11px;">${timeStr}</span></td>
          <td><span style="font-family: monospace; font-size:11px; color:#a855f7;">${log.description}</span></td>
        </tr>
      `;
    });
  } catch (err) {
    console.error(err);
  }
}

async function fetchDeveloperReports() {
  try {
    const res = await fetch(`${API_BASE}/reports`);
    const list = await res.json();
    const tbody = document.getElementById('dev-reports-table-body');
    tbody.innerHTML = '';

    if (list.length === 0) {
      tbody.innerHTML = '<tr><td colspan="3" class="text-center text-muted">No previously generated reports.</td></tr>';
      return;
    }

    list.forEach(rep => {
      const repDate = new Date(rep.report_date).toLocaleDateString('en-US', { 
        weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' 
      });
      tbody.innerHTML += `
        <tr>
          <td><strong>${repDate}</strong></td>
          <td><pre style="font-family: monospace; font-size:11px; color:var(--text-secondary); max-height:100px; overflow-y:auto; white-space:pre-wrap;">${rep.report_summary}</pre></td>
          <td><span class="text-muted" style="font-size:12px;">${new Date(rep.generated_at).toLocaleString()}</span></td>
        </tr>
      `;
    });
  } catch (err) {
    console.error(err);
  }
}

function switchDevTab(tabId) {
  document.querySelectorAll('.developer-sidebar .nav-btn').forEach(btn => btn.classList.remove('active'));
  document.getElementById(`btn-${tabId}`).classList.add('active');
  
  document.querySelectorAll('.dev-tab-content').forEach(content => content.classList.remove('active'));
  document.getElementById(`tab-${tabId}`).classList.add('active');

  const title = document.getElementById('dev-page-title');
  const subtitle = document.getElementById('dev-page-subtitle');
  
  if (tabId === 'dev-stats') {
    title.textContent = 'Dashboard & Statistics';
    subtitle.textContent = 'General metrics and direct inspection of MySQL database objects';
    fetchDeveloperStats();
    fetchDeveloperRawAppointments();
  } else if (tabId === 'dev-logs') {
    title.textContent = 'MySQL Trigger Audit Logs';
    subtitle.textContent = 'Audit trails populated entirely by triggers after_appointment_insert and after_appointment_update';
    fetchDeveloperLogs();
  } else if (tabId === 'dev-reports') {
    title.textContent = 'Saved Agenda Reports';
    subtitle.textContent = 'History of reports compiled by the cursor Stored Procedure';
    fetchDeveloperReports();
  } else if (tabId === 'dev-schema') {
    title.textContent = 'SQL Code Schema';
    subtitle.textContent = 'Review the Trigger, Stored Procedure, and View SQL definitions';
  }
}


// ====================================================================
// SYSTEM UTILITIES (ALERTS & STATUS)
// ====================================================================
function showAlert(message, type = 'success') {
  const banner = document.getElementById('alert-banner');
  const text = document.getElementById('alert-text');
  
  text.textContent = message;
  banner.className = 'alert-banner'; // Clear previous classes
  
  if (type === 'error') {
    banner.classList.add('error');
  } else {
    banner.classList.add('success');
  }
  
  banner.classList.remove('hidden');
  
  // Auto dismiss after 5 seconds
  if (window.alertTimeout) clearTimeout(window.alertTimeout);
  window.alertTimeout = setTimeout(closeAlert, 5000);
}

function closeAlert() {
  const banner = document.getElementById('alert-banner');
  banner.classList.add('hidden');
}

function setDBStatus(isConnected) {
  const landingBadge = document.getElementById('landing-db-status');
  if (!landingBadge) return;
  
  if (isConnected) {
    landingBadge.className = 'db-status-badge';
    landingBadge.innerHTML = '<span class="pulse-indicator"></span> Connected to MySQL';
  } else {
    landingBadge.className = 'db-status-badge';
    landingBadge.style.color = '#ef4444';
    landingBadge.innerHTML = '<i class="fa-solid fa-circle-xmark" style="color:#ef4444"></i> Disconnected';
  }
}
