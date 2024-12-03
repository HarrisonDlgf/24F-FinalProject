CREATE DATABASE IF NOT EXISTS StartUpConnect;

SHOW DATABASES;

USE StartUpConnect;

CREATE TABLE IF NOT EXISTS CommunicationHistory(
    MessageID INTEGER PRIMARY KEY NOT NULL,
    MessageType varchar(100) NOT NULL,
    Timestamp DATETIME DEFAULT current_timestamp,
    MessageContent varchar(200) NOT NULL

);

CREATE TABLE IF NOT EXISTS Industry (
    IndustryID INTEGER PRIMARY KEY NOT NULL,
    IndustryName varchar(75) NOT NULL,
    Description varchar(150)
);

CREATE TABLE IF NOT EXISTS Student (
    StudentID INTEGER PRIMARY KEY NOT NULL,
    Name varchar(75) NOT NULL,
    Location varchar(75) NOT NULL,
    ExperienceLevel varchar(150) NOT NULL,
    WorthAuthorization varchar(75) NOT NULL,
    EngagementScore INTEGER NOT NULL,
    Communication INTEGER NOT NULL,

    CONSTRAINT fk_messageID FOREIGN KEY (Communication)
        REFERENCES CommunicationHistory (MessageID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Skills (
    SkillID INTEGER PRIMARY KEY NOT NULL,
    SkillName varchar(75) NOT NULL,
    SkillLevel varchar(75) NOT NULL
);


CREATE TABLE IF NOT EXISTS StudentSkills (
    SkillID INTEGER NOT NULL,
    StudentID INTEGER NOT NULL,

    PRIMARY KEY (SkillID, StudentID),
    CONSTRAINT fk_studentID FOREIGN KEY (StudentID)
        REFERENCES Student (StudentID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
     CONSTRAINT fk_skillsID FOREIGN KEY (SkillID)
        REFERENCES Skills (SkillID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Startups (
    StartupID INTEGER PRIMARY KEY NOT NULL,
    Name varchar(75) NOT NULL,
    WebsiteURL varchar(100) NOT NULL,
    Rating float(1,1) NOT NULL,
    FundingStage varchar(75) NOT NULL,
    IndustryID INTEGER NOT NULL,
    Communication INTEGER NOT NULL,

    CONSTRAINT fk_industryID FOREIGN KEY (IndustryID)
        REFERENCES Industry (IndustryID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_communicationID FOREIGN KEY (Communication)
        REFERENCES CommunicationHistory (MessageID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Positions (
    JobID INTEGER PRIMARY KEY NOT NULL,
    PositionTitle varchar(75) NOT NULL,
    ContactEmail varchar(50) NOT NULL,
    ExperienceRequired varchar(100) NOT NULL,
    Industry varchar(75) NOT NULL,
    Location varchar(75) NOT NULL,
    StartDate DATETIME NOT NULL,
    Skills varchar(150) NOT NULL,
    SalaryRange varchar(50) NOT NULL,
    PositionType varchar(150) NOT NULL,
    StartUpID INTEGER NOT NULL,

    CONSTRAINT fk_startupID FOREIGN KEY (StartUpID)
        REFERENCES Startups (StartupID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS JobListingSkills (
    SkillsID INTEGER NOT NULL,
    JobID INTEGER NOT NULL,

    PRIMARY KEY (SkillsID, JobID),
    CONSTRAINT fk_jobID FOREIGN KEY (jobID)
        REFERENCES Positions (JobID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
     CONSTRAINT fk_skillsIDListing FOREIGN KEY (SkillsID)
        REFERENCES Skills (SkillID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Applications (
    ApplicationID INTEGER PRIMARY KEY NOT NULL,
    StudentID INTEGER NOT NULL,
    JobID INTEGER NOT NULL,
    SubmissionDate DATETIME NOT NULL,
    Status ENUM('ACCEPTED', 'REJECTED', 'UNDER REVIEW') NOT NULL,

    CONSTRAINT fk_jobIDApp FOREIGN KEY (jobID)
        REFERENCES Positions (JobID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_studentIDApp FOREIGN KEY (StudentID)
        REFERENCES Student (StudentID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Feedback (
    FeedbackID INTEGER PRIMARY KEY NOT NULL,
    Rating INTEGER NOT NULL,
    Comments VARCHAR(75) NOT NULL,
    SubmittedBy VARCHAR(75) NOT NULL,
    SubmittedFor VARCHAR(75) NOT NULL,
    JobID INTEGER NOT NULL,

    CONSTRAINT fk_jobIDFeedback FOREIGN KEY (jobID)
        REFERENCES Positions (JobID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS WorkExperiences (
    ExperienceID INTEGER PRIMARY KEY NOT NULL,
    StudentID INTEGER NOT NULL,
    StartDate DATETIME NOT NULL,
    EndDate DATETIME NOT NULL,
    JobID INTEGER NOT NULL,
    Feedback INTEGER NOT NULL,

    CONSTRAINT fk_jobIDWork FOREIGN KEY (jobID)
        REFERENCES Positions (JobID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_studentIDWork FOREIGN KEY (StudentID)
        REFERENCES Student (StudentID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
     CONSTRAINT fk_feedbackID FOREIGN KEY (Feedback)
        REFERENCES Feedback (FeedbackID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);


