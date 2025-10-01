import { useState } from 'react';
import { Form, Input, Button, message } from 'antd';
import { useNavigate, useParams } from 'react-router';
import { TitlesService, type CopyCreate } from '../../api';

export default function CopyCreatePage() {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { titleId } = useParams<{ titleId: string }>();

  const handleSubmit = async (values: CopyCreate) => {
    if (!titleId) return;
    
    try {
      setLoading(true);
      await TitlesService.createANewCopyOfATitle({ titleId, payload: values });
      message.success('Thêm bản sao thành công');
      navigate(`/titles/${titleId}/copies`);
    } catch (error) {
      message.error('Không thể thêm bản sao');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Thêm bản sao mới</h1>
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        style={{ maxWidth: 600 }}
      >
        <Form.Item
          name="code"
          label="Mã sách"
          rules={[{ required: true, message: 'Vui lòng nhập mã sách' }]}
        >
          <Input placeholder="Nhập mã sách" />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading}>
            Thêm
          </Button>
          <Button style={{ marginLeft: 8 }} onClick={() => navigate(`/titles/${titleId}/copies`)}>
            Hủy
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}