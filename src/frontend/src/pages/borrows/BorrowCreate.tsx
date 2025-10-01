import { useState, useEffect } from 'react';
import { Form, Select, Button, message } from 'antd';
import { useNavigate, useSearchParams } from 'react-router';
import { BorrowsService, PatronsService, TitlesService, type BorrowCreate, type Patron, type Title, type Copy } from '../../api';

const { Option } = Select;

export default function BorrowCreatePage() {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [patrons, setPatrons] = useState<Patron[]>([]);
  const [titles, setTitles] = useState<Title[]>([]);
  const [copies, setCopies] = useState<Copy[]>([]);
  const [selectedTitle, setSelectedTitle] = useState<string | undefined>();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  useEffect(() => {
    fetchPatrons();
    fetchTitles();
    
    // Pre-fill from URL params
    const titleId = searchParams.get('titleId');
    const copyId = searchParams.get('copyId');
    
    if (titleId) {
      setSelectedTitle(titleId);
      fetchCopies(titleId);
      form.setFieldValue('titleId', titleId);
    }
    
    if (copyId) {
      form.setFieldValue('copyId', copyId);
    }
  }, [searchParams, form]);

  const fetchPatrons = async () => {
    try {
      const data = await PatronsService.getAllPatrons({});
      setPatrons(data || []);
    } catch (error) {
      message.error('Không thể tải danh sách người dùng');
    }
  };

  const fetchTitles = async () => {
    try {
      const data = await TitlesService.getAllTitles({});
      setTitles(data || []);
    } catch (error) {
      message.error('Không thể tải danh sách đầu sách');
    }
  };

  const fetchCopies = async (titleId: string) => {
    try {
      const data = await TitlesService.getAllCopiesOfATitle({ titleId });
      // Only show available copies
      const availableCopies = (data || []).filter(copy => copy.status === 'AVAILABLE');
      setCopies(availableCopies);
    } catch (error) {
      message.error('Không thể tải danh sách bản sao');
    }
  };

  const handleTitleChange = (titleId: string) => {
    setSelectedTitle(titleId);
    form.setFieldValue('copyId', undefined); // Reset copy selection
    fetchCopies(titleId);
  };

  const handleSubmit = async (values: any) => {
    try {
      setLoading(true);
      const payload: BorrowCreate = {
        patronId: values.patronId,
        copyId: values.copyId
      };
      
      await BorrowsService.createANewBorrow({ payload });
      message.success('Cho mượn sách thành công');
      navigate('/borrows');
    } catch (error) {
      message.error('Không thể cho mượn sách');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Cho mượn sách</h1>
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        style={{ maxWidth: 600 }}
      >
        <Form.Item
          name="patronId"
          label="Người mượn"
          rules={[{ required: true, message: 'Vui lòng chọn người mượn' }]}
        >
          <Select placeholder="Chọn người mượn">
            {patrons.map(patron => (
              <Option key={patron.id} value={patron.id!}>{patron.name}</Option>
            ))}
          </Select>
        </Form.Item>

        <Form.Item
          name="titleId"
          label="Đầu sách"
          rules={[{ required: true, message: 'Vui lòng chọn đầu sách' }]}
        >
          <Select placeholder="Chọn đầu sách" onChange={handleTitleChange}>
            {titles.map(title => (
              <Option key={title.id} value={title.id!}>{title.name} (Tái bản {title.edition})</Option>
            ))}
          </Select>
        </Form.Item>

        <Form.Item
          name="copyId"
          label="Bản sao"
          rules={[{ required: true, message: 'Vui lòng chọn bản sao' }]}
        >
          <Select placeholder="Chọn bản sao" disabled={!selectedTitle}>
            {copies.map(copy => (
              <Option key={copy.id} value={copy.id!}>Mã: {copy.code}</Option>
            ))}
          </Select>
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading}>
            Cho mượn
          </Button>
          <Button style={{ marginLeft: 8 }} onClick={() => navigate('/borrows')}>
            Hủy
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}