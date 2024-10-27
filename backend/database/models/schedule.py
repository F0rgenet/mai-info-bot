from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base


class Entry(Base):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="RESTRICT"), nullable=False, index=True)
    subject = relationship("Subject", back_populates="entries")

    type_id = Column(Integer, ForeignKey("types.id", ondelete="RESTRICT"), nullable=False, index=True)
    type = relationship("Type", back_populates="entries")

    classroom_id = Column(Integer, ForeignKey("classrooms.id", ondelete="SET NULL"), index=True)
    classroom = relationship("Classroom", back_populates="entries")

    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="SET NULL"), index=True)
    teacher = relationship("Teacher", back_populates="entries")

    week_id = Column(Integer, ForeignKey("weeks.id", ondelete="RESTRICT"), nullable=False, index=True)
    week = relationship("Week", back_populates="entries")

    group_id = Column(Integer, ForeignKey("groups.id", ondelete="RESTRICT"), nullable=False, index=True)
    group = relationship("Group", back_populates="entries")

    __table_args__ = (
        CheckConstraint('end_datetime > start_datetime', name='check_dates_order'),
    )

    def __repr__(self):
        return f"<Entry {self.id}: {self.subject.name} {self.start_datetime}>"

    def __str__(self):
        return f"Entry {self.subject.name} at {self.start_datetime}"


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    abbreviation_id = Column(Integer, ForeignKey("abbreviations.id", ondelete="SET NULL"), index=True)
    abbreviation = relationship("Abbreviation", back_populates="subjects")

    entries = relationship("Entry", back_populates="subject", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Subject {self.id}: {self.name}>"

    def __str__(self):
        return self.name


class Abbreviation(Base):
    __tablename__ = "abbreviations"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, index=True)
    short_name = Column(String(10), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    subjects = relationship("Subject", back_populates="abbreviation")

    __table_args__ = (
        CheckConstraint('length(short_name) <= length(name)', name='check_short_name_length'),
    )

    def __repr__(self):
        return f"<Abbreviation {self.id}: {self.short_name}>"

    def __str__(self):
        return f"{self.short_name} ({self.name})"


class Type(Base):
    __tablename__ = 'types'

    id = Column(Integer, primary_key=True)
    short_name = Column(String(5), unique=True, nullable=False, index=True)
    full_name = Column(String(20), index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    entries = relationship("Entry", back_populates="type", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Type {self.id}: {self.short_name}>"

    def __str__(self):
        return self.full_name or self.short_name


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(15), unique=True, nullable=False, index=True)
    department = Column(String(15), index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    entries = relationship("Entry", back_populates="group", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Group {self.id}: {self.name}>"

    def __str__(self):
        return f"{self.name} ({self.department})" if self.department else self.name


class Week(Base):
    __tablename__ = 'weeks'

    id = Column(Integer, primary_key=True)
    number = Column(Integer, unique=True, nullable=False, index=True)
    start_date = Column(Date, nullable=False, index=True)
    end_date = Column(Date, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    entries = relationship("Entry", back_populates="week", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint('end_date > start_date', name='check_week_dates'),
        CheckConstraint('number > 0', name='check_week_number_positive'),
    )

    def __repr__(self):
        return f"<Week {self.id}: {self.number}>"

    def __str__(self):
        return f"Week {self.number} ({self.start_date} - {self.end_date})"


class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(50), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    entries = relationship("Entry", back_populates="teacher")

    def __repr__(self):
        return f"<Teacher {self.id}: {self.full_name}>"

    def __str__(self):
        return self.full_name


class Classroom(Base):
    __tablename__ = 'classrooms'

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    entries = relationship("Entry", back_populates="classroom")

    def __repr__(self):
        return f"<Classroom {self.id}: {self.name}>"

    def __str__(self):
        return self.name