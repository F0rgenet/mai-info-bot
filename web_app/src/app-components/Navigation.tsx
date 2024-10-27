import {Button} from "@/components/ui/button";
import {Select, SelectContent, SelectItem, SelectTrigger, SelectValue} from "@/components/ui/select";
import {Separator} from "@/components/ui/separator"
import {ChevronLeft, ChevronRight, Home, Menu} from "lucide-react";
import ViewControls from "@/app-components/ViewControls.tsx";

const Navigation = () => (
    <div className="p-4 space-y-4">
        <div className="grid grid-cols-2 gap-4">
            <Button className="row-span-2 h-full justify-start font-normal bg-white" variant="outline">
                <Menu className="mr-2 h-4 w-4 text-primary"/>
                Выбор группы
            </Button>

            <Select>
                <SelectTrigger className="w-full bg-white">
                    <SelectValue placeholder="Неделя"/>
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="current">Текущая неделя</SelectItem>
                    <SelectItem value="next">Следующая неделя</SelectItem>
                </SelectContent>
            </Select>

            <div className="flex space-x-2">
                <Button className="flex-1 bg-white text-primary" size="icon" variant="outline"><ChevronLeft/></Button>
                <Button className="flex-1 bg-white text-primary" size="icon" variant="outline"><Home/></Button>
                <Button className="flex-1 bg-white text-primary" size="icon" variant="outline"><ChevronRight/></Button>
            </div>
        </div>
        <ViewControls/>
        <Separator/>
    </div>
);

export default Navigation;