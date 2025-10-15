import { useState } from 'react';
import { Form, Input, Button, message } from 'antd';
import { useNavigate } from 'react-router';
import { PatronsService, type PatronCreate } from '../../api';

export default function PatronCreatePage() {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (values: PatronCreate) => {
    try {
      setLoading(true);
      await PatronsService.postCollection({ payload: values });
      message.success('Thêm người dùng thành công');
      navigate('/patrons');
    } catch (error) {
      message.error('Không thể thêm người dùng');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Thêm người dùng mới</h1>
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
            Thêm
          </Button>
          <Button style={{ marginLeft: 8 }} onClick={() => navigate('/patrons')}>
            Hủy
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}