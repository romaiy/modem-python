import React from 'react';
import { render, fireEvent, getByTestId } from '@testing-library/react';
import '@testing-library/jest-dom'
import axios from 'axios';
import FileUpload from '../components/FileUpload';

jest.mock('axios');

describe('FileUpload', () => {
  it('renders', () => {
    const { getByText } = render(<FileUpload />);
    expect(getByText('Приложение модем')).toBeInTheDocument();
  });

  it('handles file upload', async () => {
    const { getByLabelText } = render(<FileUpload />);
    const input = getByLabelText('Выберите файл');
    const file = new File(['test'], 'test.txt', { type: 'text/plain' });
    fireEvent.change(input, { target: { files: [file] } });
    expect(axios.post).toHaveBeenCalledTimes(1);
    expect(axios.post.mock.calls[0][0]).toBe('http://127.0.0.1:8000/transmitte');
    expect(axios.post.mock.calls[0][1]).toBeInstanceOf(FormData);
  });

  it('handles clear', async () => {
    const { getByLabelText, queryByText } = render(<FileUpload />);
    const input = getByLabelText('Выберите файл');
    const file = new File(['test'], 'test.txt', { type: 'text/plain' });
    fireEvent.change(input, { target: { files: [file] } });
    const clearButton = getByLabelText('Очистить');
    fireEvent.click(clearButton);
    expect(queryByText('test')).not.toBeInTheDocument();
  });
});