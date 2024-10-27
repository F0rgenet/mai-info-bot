import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Bell, ChevronLeft, MapPin, Menu, User } from "lucide-react";
import IconWithText from "@/app-components/IconWithText.tsx";
import Navigation from "@/app-components/Navigation.tsx";

interface LessonTypeProps {
    type: string;
}

const LessonType: React.FC<LessonTypeProps> = ({ type }) => {
    const typeStyles: Record<string, string> = {
        'ПЗ': 'bg-lesson-pz text-foreground',
        'ЛР': 'bg-lesson-lr text-foreground',
        'ЛК': 'bg-lesson-lk text-foreground',
        'ЭКЗ': 'bg-lesson-ekz text-foreground'
    };

    return (
        <span
            className={`px-3 py-1 rounded-full text-sm font-bold ${typeStyles[type] || 'bg-muted text-muted-foreground'}`}>
            {type}
        </span>
    );
};

interface ClassItemProps {
    subject: string;
    type: string;
    time: string;
    location: string;
    instructor: string;
    number: number;
}

const ClassItem: React.FC<ClassItemProps> = ({ subject, type, time, location, instructor, number }) => (
    <Card className="relative overflow-hidden border hover:border-primary">
        <CardContent className="p-4 space-y-1">
            <div className="flex justify-between items-start">
                <h2 className="text-lg font-semibold text-card-foreground line-clamp-2">{subject}</h2>
                <LessonType type={type} />
            </div>
            <div className="space-y-2">
                <div className="flex space-x-5">
                    <IconWithText Icon={Bell} text={time} placeholder="Не указано" />
                    <IconWithText Icon={MapPin} text={location} placeholder="Не указано" />
                </div>
                <IconWithText Icon={User} text={instructor} placeholder="Не указано" />
            </div>
            <div className="absolute bottom-4 right-4">
                <span className="text-primary opacity-50 text-3xl font-medium pr-1.5">{number}</span>
            </div>
        </CardContent>
    </Card>
);

const App: React.FC = () => {
    return (
        <div className="max-w-2xl mx-auto bg-background text-foreground min-h-screen">
            <div className="flex items-center justify-between p-4 border-b">
                <Button variant="ghost" size="icon"><Menu /></Button>
                <h1 className="text-lg font-semibold">Расписание МАИ</h1>
                <Button variant="ghost" size="icon"><ChevronLeft /></Button>
            </div>
            <Navigation />
            <div className="space-y-4 pl-4 pr-4 pb-4">
                <ClassItem
                    subject="ПНЯВУ"
                    type="ПЗ"
                    time="09:00 — 10:30"
                    location=""
                    instructor="Склеймин Юрий Александрович"
                    number={1}
                />
                <ClassItem
                    subject="Общая физика"
                    type="ЛР"
                    time="09:00 — 10:30"
                    location="3 — 404"
                    instructor=""
                    number={2}
                />
                <ClassItem
                    subject="Диф. уравнения"
                    type="ЛК"
                    time="09:00 — 10:30"
                    location="3 — 404"
                    instructor="Склеймин Юрий Александрович"
                    number={3}
                />
                <ClassItem
                    subject="Диф. уравнения"
                    type="ЭКЗ"
                    time="09:00 — 10:30"
                    location="3 — 404"
                    instructor="Склеймин Юрий Александрович"
                    number={4}
                />
            </div>
        </div>
    );
}

export default App;
