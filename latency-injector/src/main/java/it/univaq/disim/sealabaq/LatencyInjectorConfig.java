package it.univaq.disim.sealabaq;


import io.opentracing.Tracer;
import io.opentracing.contrib.spring.web.starter.ServerTracingAutoConfiguration;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.AutoConfigureAfter;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurerAdapter;


import java.io.InputStream;


@Configuration
@AutoConfigureAfter(ServerTracingAutoConfiguration.class)
public class LatencyInjectorConfig extends WebMvcConfigurerAdapter{

    private static final Log logger = LogFactory.getLog(LatencyInjectorConfig.class);

    @Autowired
    private Tracer tracer;

    private InputStream stream = getClass().getClassLoader().getResourceAsStream("/config.json");


    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        LatencyInjectorConfig.logger.info("Adding Interceptor" + LatencyInjectionInterceptor.class.getSimpleName());
        registry.addInterceptor(new LatencyInjectionInterceptor(tracer, stream));
    }

}
