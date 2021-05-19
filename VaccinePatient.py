from VaccineReservationScheduler import VaccineReservationScheduler as scheduler
from COVID19_vaccine import COVID19Vaccine as covid
class VaccinePatient:
	def __init__(self, cursor, patientid):
		self.covid = covid()
		self.patientid = patientid
		self.getPatientInfo = "SELECT V.DosesPerPatient, VA.DoseNumber FROM Vaccines AS V, VaccineAppointments AS VA WHERE VA.VaccineAppointmentId=%s AND VA.VaccineName = V.VaccineName"

	def ReserveAppointment():
		return None

	def ScheduleAppointment(cursor, slotid):
		self.getPatientInfo = "SELECT V.DosesPerPatient AS DosesPerPatient, VA.DoseNumber AS DoseNumber FROM Vaccines AS V, VaccineAppointments AS VA WHERE VA.VaccineAppointmentId=%s AND VA.VaccineName = V.VaccineName"
		cursor.execute(self.getPatientInfo)
		row = cursor.fetchone()
		dose_number = row['DoseNumber']
		doses_per_patient = row['DosesPerPatient']
		if does_number > doses_per_patient:
			raise Exception('Patient dose number exceeds maxiumum number of doses per patient for this vaccine.')
		if dose_number = 1:
			covid.ReserveDoses(slotid)
		scheduler.ScheduleAppointmentSlot(slotid, cursor)
		print('Appointment successfully scheduled.')
		return None