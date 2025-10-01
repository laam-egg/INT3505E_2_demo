import { useState, useEffect } from 'react';
import { Form, Input, Button, message, Spin } from 'antd';
import { useNavigate, useParams } from 'react-router';
import { TitlesService, type Copy, type CopyUpdate } from '../../api';

export default function CopyUpdatePage() {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [copy, setCopy] = useState<Copy | null>(null);
  const navigate = useNavigate();
  const { titleId, copyId } = useParams<{ titleId: string; copyId: string }>();

  useEffect(() => {
    if (titleId && copyId) {
      fetchCopy();
    }
  }, [titleId, copyId]);

  const fetchCopy = async () => {
    if (!titleId || !copyId) return;
    try {
      setLoading(true);
      const data = await TitlesService.getCopyById({ titleId, copyId });
      setCopy(data);
      form.setFieldsValue(data);
    } catch (error) {
      message.error('Không thể tải thông tin bản sao');
      navigate(`/titles/${titleId}/copies`);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (values: CopyUpdate) => {
    if (!titleId || !copyId) return;

    try {
      setLoading(true);
      await TitlesService.updateCopyById({ titleId, copyId, payload: values });
      message.success('Cập nhật bản sao thành công');
      navigate(`/titles/${titleId}/copies`);
    } catch (error) {
      message.error('Không thể cập nhật bản sao');
    } finally {
      setLoading(false);
    }
  };

  if (!copy) {
    return <Spin size="large" style={{ display: 'block', textAlign: 'center', marginTop: 100 }} />;
  }

  return (
    <div>
      <h1>Chỉnh sửa bản sao</h1>
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
            Cập nhật
          </Button>
          <Button style={{ marginLeft: 8 }} onClick={() => navigate(`/titles/${titleId}/copies`)}>
            Hủy
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}