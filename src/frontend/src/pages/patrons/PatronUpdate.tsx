import { useState, useEffect } from 'react';
import { Form, Input, Button, message, Spin } from 'antd';
import { useNavigate, useParams } from 'react-router';
import { PatronsService, type Patron, type PatronUpdate } from '../../api';

export default function PatronUpdatePage() {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [patron, setPatron] = useState<Patron | null>(null);
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();

  useEffect(() => {
    if (id) {
      fetchPatron(id);
    }
  }, [id]);

  const fetchPatron = async (patronId: string) => {
    try {
      setLoading(true);
      const data = await PatronsService.getPatronById({ patronId });
      setPatron(data);
      form.setFieldsValue(data);
    } catch (error) {
      message.error('Không thể tải thông tin người dùng');
      navigate('/patrons');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (values: PatronUpdate) => {
    if (!id) return;

    try {
      setLoading(true);
      await PatronsService.updatePatronById({ patronId: id, payload: values });
      message.success('Cập nhật người dùng thành công');
      navigate('/patrons');
    } catch (error) {
      message.error('Không thể cập nhật người dùng');
    } finally {
      setLoading(false);
    }
  };

  if (!patron) {
    return <Spin size="large" style={{ display: 'block', textAlign: 'center', marginTop: 100 }} />;
  }

  return (
    <div>
      <h1>Chỉnh sửa thông tin người dùng</h1>
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        style={{ maxWidth: 600 }}
      >
        <Form.Item
          name="name"
          label="Tên người dùng"
          rules={[{ required: true, message: 'Vui lòng nhập tên người dùng' }]}
        >
          <Input placeholder="Nhập tên người dùng" />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading}>
            Cập nhật
          </Button>
          <Button style={{ marginLeft: 8 }} onClick={() => navigate('/patrons')}>
            Hủy
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}