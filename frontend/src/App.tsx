import React, { useState } from "react";
import Plot from "react-plotly.js";
import "./App.css";
import { message, Form, Button, Row } from "antd";
import { Formik } from "formik";
import { FormItem, DatePicker, Select } from "formik-antd";
import { Typography } from "antd";

const { Title, Text } = Typography;

interface DataPoint {
  datelabel: Date | number | string;
  value: number | string;
}

type DataPoints = DataPoint[];

interface ServiceInit {
  status: "init";
}
interface ServiceLoading {
  status: "loading";
}
interface ServiceLoaded<T> {
  status: "loaded";
  payload: T;
}
interface ServiceError {
  status: "error";
  error: Error | string;
}

type Service<T> =
  | ServiceInit
  | ServiceLoading
  | ServiceLoaded<T>
  | ServiceError;

const App = () => {
  const [result, setResult] = useState<Service<DataPoints>>({
    status: "loading"
  });

  const makeRequest = (
    startTime: Date,
    endTime: Date,
    productionTime: number
  ) => {
    console.log(startTime, endTime, productionTime);
    // const data = fetch("", {qs: { startTime, endTime, productionTime} })
    //   .then(response => response.json())
    //   .then(response =>
    //     setResult({
    //       status: "loaded",
    //       payload: response
    //     })
    //   )
    //   .catch(error =>
    //     setResult({
    //       status: "error",
    //       error
    //     })
    //   );
    return true;
  };

  return (
    <div
      className="App"
      style={{
        textAlign: "center",
        height: "100vh",
        display: "flex",
        alignItems: "center"
      }}
    >
      <Row style={{ margin: "0 auto" }}>
        <Title>Zero Emissions Factory</Title>
        <Text>
          A scheduler to optimize production lines with local green energy
          prodviders
        </Text>
        {
          <Formik
            initialValues={{
              startTime: new Date(),
              endTime: new Date(),
              productionTime: 0 //minutes
            }}
            onSubmit={async (values: any, actions: any) => {
              actions.setSubmitting(true);
              if (values) {
                const { startTime, endTime, productionTime } = values;
                const response = await makeRequest(
                  startTime,
                  endTime,
                  productionTime
                );
                if (response) {
                  message.success("response");
                  actions.setSubmitting(false);
                } else {
                  message.error("Backend error");
                  actions.setSubmitting(false);
                }
              }
              // message.error("Missing form data front end");
              // actions.setSubmitting(false);
            }}
            render={({ handleSubmit, isSubmitting, isValid }) => (
              <Form onSubmit={handleSubmit}>
                <FormItem name="startTime" label="Start Time">
                  <DatePicker name="startTime" style={{ width: 200 }} />
                </FormItem>
                <FormItem name="endTime" label="End Time">
                  <DatePicker name="endTime" style={{ width: 200 }} />
                </FormItem>
                <FormItem
                  name="productionTime"
                  label="Approximate Production Time"
                >
                  <Select name="productionTime" style={{ width: 200 }}>
                    {Select.renderOptions(
                      [15, 30, 45, 60].map(duration => ({
                        value: duration,
                        label: <span>{duration.toString() + " minutes"}</span>
                      }))
                    )}
                  </Select>
                </FormItem>
                <Form.Item>
                  <Button
                    icon="check"
                    type="primary"
                    style={{ background: "#1DA57A", border: "#1DA57A" }}
                    loading={isSubmitting}
                    disabled={!isValid}
                    onClick={() => {
                      handleSubmit();
                    }}
                  >
                    Optimize production
                  </Button>
                </Form.Item>
              </Form>
            )}
          />

          // <Plot
          //   data={[
          //     {
          //       x: result.payload.map(label => label),
          //       y: result.payload.map((_, value) => value),
          //       type: "bar",
          //       marker: { color: "green" }
          //     },
          //     { type: "bar", x: [1, 2, 3], y: [2, 5, 3] }
          //   ]}
          //   layout={{
          //     width: 450,
          //     height: 450,
          //     title: "Percentage of green energy"
          //   }}
          // />
        }
      </Row>
    </div>
  );
};

export default App;
