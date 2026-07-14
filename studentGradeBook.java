import java.util.*;

class Student {
    private String id;
    private String name;
    private Map<String, Double> grades;

    public Student(String id, String name) {
        this.id = id;
        this.name = name;
        this.grades = new LinkedHashMap<>();
    }

    public String getId() {
        return id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void addGrade(String subject, double marks) {
        grades.put(subject, marks);
    }

    public double getAverage() {
        if (grades.isEmpty()) {
            return 0;
        }

        double total = 0;
        for (double mark : grades.values()) {
            total += mark;
        }
        return total / grades.size();
    }

    public void displayReport() {
        System.out.println("\nStudent ID: " + id);
        System.out.println("Name: " + name);
        System.out.println("Grades:");

        if (grades.isEmpty()) {
            System.out.println("No grades available.");
        } else {
            for (Map.Entry<String, Double> entry : grades.entrySet()) {
                System.out.println(entry.getKey() + ": " + entry.getValue());
            }
            System.out.println("Average Score: " + getAverage());
            System.out.println("Final Grade: " + calculateLetterGrade());
        }
    }

    private String calculateLetterGrade() {
        double avg = getAverage();

        if (avg >= 90) return "A";
        else if (avg >= 80) return "B";
        else if (avg >= 70) return "C";
        else if (avg >= 60) return "D";
        else return "F";
    }
}

public class studentGradeBook {
    private static Scanner scanner = new Scanner(System.in);
    private static ArrayList<Student> students = new ArrayList<>();

    public static void main(String[] args) {
        int choice;

        do {
            System.out.println("\n===== STUDENT GRADEBOOK =====");
            System.out.println("1. Add Student");
            System.out.println("2. Add Subject Grade");
            System.out.println("3. Edit Student Name");
            System.out.println("4. Remove Student");
            System.out.println("5. Display Student Report");
            System.out.println("6. Display All Reports");
            System.out.println("7. Exit");
            System.out.print("Enter your choice: ");

            choice = scanner.nextInt();
            scanner.nextLine();

            switch (choice) {
                case 1:
                    addStudent();
                    break;
                case 2:
                    addSubjectGrade();
                    break;
                case 3:
                    editStudent();
                    break;
                case 4:
                    removeStudent();
                    break;
                case 5:
                    displayStudentReport();
                    break;
                case 6:
                    displayAllReports();
                    break;
                case 7:
                    System.out.println("Exiting Gradebook...");
                    break;
                default:
                    System.out.println("Invalid choice. Try again.");
            }

        } while (choice != 7);
    }

    private static void addStudent() {
        System.out.print("Enter Student ID: ");
        String id = scanner.nextLine();

        if (findStudent(id) != null) {
            System.out.println("Student ID already exists.");
            return;
        }

        System.out.print("Enter Student Name: ");
        String name = scanner.nextLine();

        students.add(new Student(id, name));
        System.out.println("Student added successfully.");
    }

    private static void addSubjectGrade() {
        System.out.print("Enter Student ID: ");
        String id = scanner.nextLine();

        Student student = findStudent(id);

        if (student == null) {
            System.out.println("Student not found.");
            return;
        }

        System.out.print("Enter Subject Name: ");
        String subject = scanner.nextLine();

        System.out.print("Enter Marks: ");
        double marks = scanner.nextDouble();
        scanner.nextLine();

        student.addGrade(subject, marks);
        System.out.println("Grade added successfully.");
    }

    private static void editStudent() {
        System.out.print("Enter Student ID: ");
        String id = scanner.nextLine();

        Student student = findStudent(id);

        if (student == null) {
            System.out.println("Student not found.");
            return;
        }

        System.out.print("Enter New Name: ");
        String newName = scanner.nextLine();

        student.setName(newName);
        System.out.println("Student updated successfully.");
    }

    private static void removeStudent() {
        System.out.print("Enter Student ID: ");
        String id = scanner.nextLine();

        Student student = findStudent(id);

        if (student == null) {
            System.out.println("Student not found.");
            return;
        }

        students.remove(student);
        System.out.println("Student removed successfully.");
    }

    private static void displayStudentReport() {
        System.out.print("Enter Student ID: ");
        String id = scanner.nextLine();

        Student student = findStudent(id);

        if (student == null) {
            System.out.println("Student not found.");
        } else {
            student.displayReport();
        }
    }

    private static void displayAllReports() {
        if (students.isEmpty()) {
            System.out.println("No student records available.");
            return;
        }

        for (Student student : students) {
            student.displayReport();
        }
    }

    private static Student findStudent(String id) {
        for (Student student : students) {
            if (student.getId().equalsIgnoreCase(id)) {
                return student;
            }
        }
        return null;
    }
}