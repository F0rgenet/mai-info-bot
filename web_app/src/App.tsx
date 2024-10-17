import '@telegram-apps/telegram-ui/dist/styles.css';

import {
    AppRoot,
    Placeholder,
    Button,
    Pagination,
    Modal,
    SegmentedControl,
    Cell,
    Divider, IconButton, Select
} from '@telegram-apps/telegram-ui';
import {
    ModalHeader
} from "@telegram-apps/telegram-ui/dist/components/Overlays/Modal/components/ModalHeader/ModalHeader";
import {
    SegmentedControlItem
} from "@telegram-apps/telegram-ui/dist/components/Navigation/SegmentedControl/components/SegmentedControlItem/SegmentedControlItem";
import {Icon20QuestionMark} from "@telegram-apps/telegram-ui/dist/icons/20/question_mark";
import {Icon28Attach} from "@telegram-apps/telegram-ui/dist/icons/28/attach";
import {Icon24ChevronLeft} from "@telegram-apps/telegram-ui/dist/icons/24/chevron_left";
import {Icon24ChevronRight} from "@telegram-apps/telegram-ui/dist/icons/24/chevron_right";


const App = () => (
  <AppRoot>
      <IconButton mode={"gray"}>
          <Icon28Attach />
          Выбор группы
      </IconButton>
      <SegmentedControl>
          <SegmentedControlItem onClick={function noRefCheck(){}} selected>День</SegmentedControlItem>
          <SegmentedControlItem onClick={function noRefCheck(){}}>Неделя</SegmentedControlItem>
      </SegmentedControl>
      <Select header="Неделя" placeholder="Выбрать">
          <option>№1</option>
          <option>№2</option>
      </Select>
      <IconButton>
          <Icon24ChevronLeft/>
      </IconButton>
      <IconButton>
          <Icon24ChevronRight/>
      </IconButton>
      <SegmentedControl>
          <SegmentedControlItem>ПН</SegmentedControlItem>
          <SegmentedControlItem>ВТ</SegmentedControlItem>
          <SegmentedControlItem>СР</SegmentedControlItem>
          <SegmentedControlItem>ЧТ</SegmentedControlItem>
          <SegmentedControlItem>ПТ</SegmentedControlItem>
          <SegmentedControlItem>СБ</SegmentedControlItem>
      </SegmentedControl>
  </AppRoot>
);

export default App;