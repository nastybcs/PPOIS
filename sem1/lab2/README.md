# Dean's Office

## Entities, Fields, Behaviors, Associations

AcademyLevel 1 0  
AttendanceStatus 3 0  
AttendanceTracker 2 3 -> Group, Attendance  
Attendance 3 1 -> Student, ScheduleEntry  
Course 5 2 -> Teacher, Student  
CreditGrade 3 0 -> Course  
Department 4 2 -> Teacher, Course  
ExamGrade 3 0 -> Course  
Faculty 6 5 -> Group, Major, Teacher, Dean  
Grade 2 0 -> Course  
Group 7 4 -> Major, Student, AttendanceTracker  
Major 5 6 -> Course, Student, Teacher  
ScholarshipRecord 4 0  
ScholarshipType 4 0  
StudentAttendance 2 1 -> Student  
StudentDebts 2 1 -> Student, Course  
StudentGrades 3 7 -> Student, Grade, ExamGrade, CreditGrade, Session  
StudentScholarship 3 2 -> Student, ScholarshipRecord, Session  
Subgroup 4 2 -> Student, Group  
Book 5 2 -> Student  
CourseProject 7 3 -> Student, Teacher, Grade  
Credit 5 1 -> Course, Location, Teacher, Student  
Document 3 2 -> Student  
Event 7 4 -> Location, Group, Student  
Exam 5 1 -> Course, Location, Teacher, Student  
Library 2 6 -> Book  
ProjectStatus 4 0  
PublicationType 4 0  
Publication 6 1 -> Teacher/Student, PublicationType  
ResearchLab 4 3 -> Teacher, Student, CourseProject  
ScientificConference 5 4 -> Teacher/Student, Publication  
ThesisArchive 1 4 -> Thesis  
Thesis 6 2 -> Student, Teacher  
ActivityType 3 0  
Building 4 3 -> Campus, Room  
Campus 3 3 -> Building  
CapacityCalculator 0 1 -> ActivityType, Group, Subgroup  
ConflictChecker 0 1 -> ScheduleEntry, Location  
Location 3 2 -> Campus, Building, Room  
Room 3 0 -> Building  
Schedule 1 3 -> Location, Teacher, Course, Group, Subgroup  
Semester 4 2 -> Schedule  
Session 6 5 -> Group, Semester, Exam, Credit, Course, Student    
Dean 5 0 -> Person, Faculty  
DocumentSecretary 5 2 -> Person, Faculty, Document  
EventSecretary 6 5 -> Person, Faculty, Event  
Leader 6 3 -> Student  
Person 3 0  
Student 12 7 -> Person, Group, Major, StudentGrades, StudentDebts, StudentScholarship, StudentAttendance, Document, ResearchLab  
Teacher 5 1 -> Person, Department, ResearchLab  

## Summary

Поля: 199  
Поведения: 107  
Ассоциации: 73
